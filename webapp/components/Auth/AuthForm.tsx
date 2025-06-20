import React, { useState } from "react";
import { Box, Button, TextField, Typography } from "@mui/material";

type AuthMode = "login" | "signup";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
interface AuthFormProps {
  mode: AuthMode;
  onSuccess: (email: string, username: string) => void;
}

const AuthForm: React.FC<AuthFormProps> = ({ mode, onSuccess }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

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

      const url = mode === "signup"
        ? `${BACKEND_URL}/signup`
        : `${BACKEND_URL}/login`;

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
        onSuccess(data.email, data.username);
      } else {
        const errData = await res.json();
        setError(errData.detail || "Authentication failed.");
      }
    } catch (err) {
      setError(`Network error. Please try again. : ${err}`);
    }
  };

  return (
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
  );
};

export default AuthForm;
