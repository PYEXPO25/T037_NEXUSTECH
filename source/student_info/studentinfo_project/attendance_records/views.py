from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from . forms import LoginForm
from . models import Attendance,Student
from attendance_records.models import Student,Attendance
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import datetime


# Create your views here.

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect(reverse("attendance_records:index"))
            
    return render(request,"attendance_records/login.html",{'title':'Login','form':form,'style':'forms'})



def index_view(request):
    students = Student.objects.all()
    for student in students:
        if Attendance.objects.filter(student=student, date=now().date()).exists():
            student.attendance = Attendance.objects.filter(student=student, date=now().date()).first()
    return render(request, 'attendance_records/index.html', {'students': students})

    
   
def logout_view(request):
    logout(request)
    return redirect(reverse("index"))

def take_attendance(request):
    import cv2
    import face_recognition
    import os
    import numpy as np
    import mediapipe as mp
    import torch
    from torchvision import transforms
    from PIL import Image
    from django . utils.timezone import now
    
    # Initialize Face Mesh once
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=100,
        refine_landmarks=True,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small", trust_repo=True).to(device).eval()

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((384, 384)),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])

    REFERENCE_DIR = r"D:\T037_NEXUSTECH\T037_NEXUSTECH\T037_NEXUSTECH\source\reference_faces"
    if not os.path.exists(REFERENCE_DIR):
        return HttpResponse(f"Error: Reference directory '{REFERENCE_DIR}' does not exist.", status=400)

    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(REFERENCE_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            person_name = os.path.splitext(filename)[0]
            img_path = os.path.join(REFERENCE_DIR, filename)
            try:
                image = face_recognition.load_image_file(img_path)
                encoding = face_recognition.face_encodings(image, model="hog", num_jitters=10)  # More jitter for better accuracy
                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_names.append(person_name)
            except Exception:
                pass

    if not known_face_encodings:
        return HttpResponse("No known faces found. Please add reference images.", status=400)
        
    cap = cv2.VideoCapture(0)
    frame_count = 0  # Track frame count for processing optimization

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 3 != 0:  # Process every 3rd frame to reduce inconsistencies
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, num_jitters=2)  # Lower jitter for speed

        results = face_mesh.process(rgb_frame) if len(face_locations) > 0 else None

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)  # Higher tolerance
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else -1
            name = "Unmatched"

            if best_match_index != -1 and matches[best_match_index] and face_distances[best_match_index] < 0.5:
                name = known_face_names[best_match_index]
           
            student = Student.objects.filter(name=name).first()
            if student:
                attendance, created = Attendance.objects.get_or_create(student=student, date=now().date())
                attendance.status = "P"
                attendance.period1 = True
                attendance.period2 = True
                attendance.period3 = True
                attendance.period4 = True
                attendance.period5 = True
                attendance.period6 = True
                attendance.period7 = True
                attendance.period8 = True
                attendance.save()
            
                print(f"Attendance marked for {name}: Present")
            else:
                print(f"Student {name} not found in database. Skipping attendance update.")
            
            color = (0, 255, 0) if name != "Unmatched" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)

        cv2.imshow("Optimized Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return redirect(reverse("attendance_records:index"))
def team_portfolio(request):
    return render(request, 'portfolio.html')