import React, { useState } from "react";
import { 
  Box, 
  Button, 
  TextField, 
  Typography, 
  Container, 
  Paper, 
  Tabs, 
  Tab 
} from "@mui/material";

type AuthMode = "login" | "signup";

const PersoVoxLoginPage: React.FC = () => {
  const [mode, setMode] = useState<AuthMode>("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleModeChange = (event: React.SyntheticEvent, newValue: AuthMode) => {
    setMode(newValue);
    setError("");
    setUsername("");
    setEmail("");
    setPassword("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
  
    try {
      // Validation
      if (mode === "signup" && (!username || !email || !password)) {
        setError("Please fill in all fields.");
        return;
      }
      if (mode === "login" && (!email || !password)) {
        setError("Please enter your email and password.");
        return;
      }
  
      // Determine endpoint and payload
      const url = mode === "signup" ? "http://localhost:8000/signup" : "http://localhost:8000/login";
  
      const payload = mode === "signup"
        ? { username, email, password }
        : { email, password };
  
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
  
      if (res.ok) {
        const data = await res.json();
        // For now, just redirect on success
        // You might want to save user info or token here later
        localStorage.setItem("user", JSON.stringify({username, email}));
        window.location.href = "/ResumeGenerator";
      } else {
        const errData = await res.json();
        setError(errData.detail || "Authentication failed.");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    }
  };
  

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper elevation={4} sx={{ p: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center" fontWeight="bold" color="primary">
          Welcome to PersoVox
        </Typography>
        <Typography variant="h6" align="center" sx={{ mb: 4 }}>
          Your personalized voice for creating standout resumes effortlessly.
        </Typography>

        <Tabs
          value={mode}
          onChange={handleModeChange}
          indicatorColor="primary"
          textColor="primary"
          centered
          sx={{ mb: 3 }}
        >
          <Tab label="Login" value="login" />
          <Tab label="Sign Up" value="signup" />
        </Tabs>

        <Box component="form" onSubmit={handleSubmit} noValidate>
          {mode === "signup" && (
            <TextField
              label="Username"
              variant="outlined"
              fullWidth
              margin="normal"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          )}
          <TextField
            label="Email"
            type="email"
            variant="outlined"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && (
            <Typography color="error" sx={{ mt: 1 }}>
              {error}
            </Typography>
          )}

          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 3 }}
          >
            {mode === "login" ? "Login" : "Create Account"}
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default PersoVoxLoginPage;
