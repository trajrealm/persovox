import React from 'react';
import { Box, Typography } from '@mui/material';

const Footer: React.FC = () => (
  <Box component="footer" sx={{ mt: 'auto', py: 3, textAlign: 'center', borderTop: '1px solid #ccc' }}>
    <Typography variant="body2" color="text.secondary">
      © {new Date().getFullYear()} PersoVox. All rights reserved.
    </Typography>
  </Box>
);

export default Footer;