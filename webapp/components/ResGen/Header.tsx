import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Menu, MenuItem, Box } from '@mui/material';
import AccountCircle from '@mui/icons-material/AccountCircle';
import { useRouter } from 'next/router';

interface HeaderProps {
  userInfo: { username: string; email: string } | null;
}

const Header: React.FC<HeaderProps> = ({ userInfo }) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const router = useRouter();

  return (
    <AppBar position="fixed" sx={{ bgcolor: '#1e1e2f' }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Typography variant="h6" sx={{ fontWeight: 700, color: '#fff' }}>
          <span style={{ color: '#00bcd4' }}>Perso</span>Vox
        </Typography>
        <Box>
          <Button href="/" sx={{ color: '#fff', mx: 1 }}>Home</Button>
          <Button href="/about" sx={{ color: '#fff', mx: 1 }}>About</Button>
          <Button href="/contact" sx={{ color: '#fff', mx: 1 }}>Contact</Button>
        </Box>
        {userInfo && (
          <>
            <IconButton onClick={(e) => setAnchorEl(e.currentTarget)} sx={{ ml: 2 }} color="inherit">
              <AccountCircle />
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={() => setAnchorEl(null)}
              anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            >
              <MenuItem disabled>
                <strong>{userInfo.username}</strong>
              </MenuItem>
              <MenuItem disabled>{userInfo.email}</MenuItem>
              <MenuItem onClick={() => {
                localStorage.removeItem('user');
                router.push('/login_signup');
              }}>
                Logout
              </MenuItem>
            </Menu>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Header;