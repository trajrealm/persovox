import React from "react";
import { Tabs, Tab } from "@mui/material";

type AuthMode = "login" | "signup";

interface AuthTabsProps {
  mode: AuthMode;
  onChange: (event: React.SyntheticEvent, newValue: AuthMode) => void;
}

const AuthTabs: React.FC<AuthTabsProps> = ({ mode, onChange }) => {
  return (
    <Tabs
      value={mode}
      onChange={onChange}
      indicatorColor="primary"
      textColor="primary"
      centered
      sx={{ mb: 3 }}
    >
      <Tab label="Login" value="login" />
      <Tab label="Sign Up" value="signup" />
    </Tabs>
  );
};

export default AuthTabs;
