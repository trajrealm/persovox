import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { saveAs } from 'file-saver';
import {
  AppBar,
  Box,
  Button,
  Container,
  CssBaseline,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Tab,
  Tabs,
  TextField,
  Toolbar,
  Typography,
  CircularProgress,
  Stack,
  Paper,
} from '@mui/material';

const BACKEND_URL = 'http://localhost:8000'; // Change if needed

const ResumeGenerator = () => {
  const [users, setUsers] = useState<string[]>([]);
  const [selectedUser, setSelectedUser] = useState('');
  const [jobLink, setJobLink] = useState('');
  const [jobText, setJobText] = useState('');
  const [resume, setResume] = useState('');
  const [coverLetter, setCoverLetter] = useState('');
  const [loading, setLoading] = useState(false);
  const [tabIndex, setTabIndex] = useState(0);

  useEffect(() => {
    axios.get(`${BACKEND_URL}/users`).then(res => setUsers(res.data.users));
  }, []);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${BACKEND_URL}/generate`, {
        user: selectedUser,
        job_link: jobLink,
        job_text: jobText,
      });
      setResume(response.data.resume);
      setCoverLetter(response.data.cover_letter);
    } catch (err) {
      alert('Error generating resume. Check console.');
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <CssBaseline />

      {/* Header */}
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
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Box component="main" sx={{ flexGrow: 1, mt: 10, px: 2 }}>
        <Container maxWidth="md">
          <Stack spacing={4}>
            <Typography variant="h4" textAlign="center" gutterBottom fontWeight={600}>
              Resume & Cover Letter Generator
            </Typography>

            <FormControl fullWidth required>
              <InputLabel id="select-user-label">Select User</InputLabel>
              <Select
                labelId="select-user-label"
                value={selectedUser}
                label="Select User"
                onChange={e => setSelectedUser(e.target.value)}
              >
                <MenuItem value="">
                  <em>-- Choose User --</em>
                </MenuItem>
                {users.map(user => (
                  <MenuItem key={user} value={user}>
                    {user}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              fullWidth
              label="Job Description URL (optional)"
              placeholder="Paste job URL"
              value={jobLink}
              onChange={e => setJobLink(e.target.value)}
            />

            <TextField
              fullWidth
              label="Or Paste Job Description Text"
              placeholder="Paste job description..."
              value={jobText}
              onChange={e => setJobText(e.target.value)}
              multiline
              minRows={6}
            />

            <Button
              variant="contained"
              color="primary"
              onClick={handleGenerate}
              disabled={!selectedUser || loading}
              startIcon={loading ? <CircularProgress size={20} /> : null}
              sx={{ alignSelf: 'start' }}
            >
              Generate Resume & Cover Letter
            </Button>

            {(resume || coverLetter) && (
              <Box>
                <Tabs value={tabIndex} onChange={(_, v) => setTabIndex(v)} centered>
                  {resume && <Tab label="Resume" />}
                  {coverLetter && <Tab label="Cover Letter" />}
                </Tabs>

                <Box mt={2}>
                  {tabIndex === 0 && resume && (
                    <>
                      <Typography variant="h5" gutterBottom>
                        Generated Resume
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 3, bgcolor: 'grey.100', maxHeight: 500, overflowY: 'auto' }}>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{resume}</ReactMarkdown>
                      </Paper>
                      <Box mt={2}>
                        <Button variant="outlined" onClick={() => downloadDocxFile('resume.docx', resume)}>
                          Download Resume (.docx)
                        </Button>
                      </Box>
                    </>
                  )}

                  {tabIndex === 1 && coverLetter && (
                    <>
                      <Typography variant="h5" gutterBottom>
                        Generated Cover Letter
                      </Typography>
                      <Paper variant="outlined" sx={{ p: 3, bgcolor: 'grey.100', maxHeight: 500, overflowY: 'auto' }}>
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{coverLetter}</ReactMarkdown>
                      </Paper>
                      <Box mt={2}>
                        <Button variant="outlined" onClick={() => downloadDocxFile('cover_letter.docx', coverLetter)}>
                          Download Cover Letter (.docx)
                        </Button>
                      </Box>
                    </>
                  )}
                </Box>
              </Box>
            )}
          </Stack>
        </Container>
      </Box>

      {/* Footer */}
      <Box component="footer" sx={{ mt: 'auto', py: 3, textAlign: 'center', borderTop: '1px solid #ccc' }}>
        <Typography variant="body2" color="text.secondary">
          &copy; {new Date().getFullYear()} PersoVox. All rights reserved.
        </Typography>
      </Box>
    </Box>
  );
};

export default ResumeGenerator;

const downloadDocxFile = async (filename: string, content: string) => {
  const blob = new Blob([content], {
    type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  });
  saveAs(blob, filename);
};
