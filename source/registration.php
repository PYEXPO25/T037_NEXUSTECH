<?php
// Database Connection
$servername = "localhost";
$username = "root"; // Default MySQL username
$password = ""; // Default MySQL password (leave empty if no password)
$dbname = "attendance_system";

// Create Connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check Connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Collect Form Data
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);
    $role = $_POST['role'];

    // Basic Validation
    if (empty($username) || empty($password) || empty($role)) {
        echo "All fields are required!";
        exit();
    }

    // Password Hashing for Security
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Insert Query
    $sql = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("sss", $username, $hashed_password, $role);

    if ($stmt->execute()) {
        echo "Registration Successful! <a href='index.html'>Login Here</a>";
    } else {
        echo "Error: " . $stmt->error;
    }

    // Close Connection
    $stmt->close();
    $conn->close();
}
?>
