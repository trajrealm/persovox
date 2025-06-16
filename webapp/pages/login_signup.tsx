import React, { useState } from "react";
import { Box, Container, Paper, Typography } from "@mui/material";

import AuthTabs from "../components/Auth/AuthTabs";
import AuthForm from "../components/Auth/AuthForm";

type AuthMode = "login" | "signup";

const PersoVoxLoginPage: React.FC = () => {
  const [mode, setMode] = useState<AuthMode>("login");

  const handleModeChange = (event: React.SyntheticEvent, newValue: AuthMode) => {
    setMode(newValue);
  };

  const handleSuccess = (email: string, username: string) => {
    localStorage.setItem("user", JSON.stringify({ email, username }));
    window.location.href = "/ResumeGenerator";
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper elevation={4} sx={{ p: 4 }}>
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          align="center"
          fontWeight="bold"
          color="primary"
        >
          Welcome to PersoVox
        </Typography>
        <Typography variant="h6" align="center" sx={{ mb: 4 }}>
          Your personalized voice for creating standout resumes effortlessly.
        </Typography>

        <AuthTabs mode={mode} onChange={handleModeChange} />
        <AuthForm mode={mode} onSuccess={handleSuccess} />
      </Paper>
    </Container>
  );
};

export default PersoVoxLoginPage;
