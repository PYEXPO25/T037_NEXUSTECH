<?php
// Database Connection
$servername = "localhost";
$username = "root";
$password = "";
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

    // Validate Fields
    if (empty($username) || empty($password) || empty($role)) {
        echo "All fields are required!";
        exit();
    }

    // Check if User Exists
    $sql = "SELECT password FROM users WHERE username=? AND role=?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $username, $role);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($hashed_password);
        $stmt->fetch();

        // Verify Password
        if (password_verify($password, $hashed_password)) {
            echo "Login Successful! Welcome, $username.";
        } else {
            echo "Invalid Credentials!";
        }
    } else {
        echo "User Not Found!";
    }

    // Close Connection
    $stmt->close();
    $conn->close();
}
?>
