import React, { useEffect, useState } from 'react';
import { Box, Container, CssBaseline, Stack, Typography } from '@mui/material';
import Header from '../components/ResGen/Header';
import FileUpload from '../components/ResGen//FileUpload';
import InputForm from '../components/ResGen/InputForm';
import OutputTabs from '../components/ResGen/OutputTabs';
import Footer from '../components/ResGen/Footer';
import { fetchResumes, fetchResumeSelections, saveResumeSelections } from '../utils/api';


const ResumeGenerator = () => {
  const [userInfo, setUserInfo] = useState<{ username: string; email: string } | null>(null);
  const [jobLink, setJobLink] = useState('');
  const [jobText, setJobText] = useState('');
  const [resume, setResume] = useState('');
  const [coverLetter, setCoverLetter] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadedResumes, setUploadedResumes] = useState<string[]>([]);
  const [selectedResumes, setSelectedResumes] = useState<string[]>([]);
  const [regenLoading, setRegenLoading] = useState(false);
  const [regenMessage, setRegenMessage] = useState('');

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (!storedUser) {
      if (process.env.NODE_ENV === 'production') {
        window.location.href = '/login';
      }
    } else {
      const user = JSON.parse(storedUser);
      setUserInfo(user);

      fetchResumes(user.username).then(resumes => {
        setUploadedResumes(resumes);
        const savedSelected = localStorage.getItem(`selectedResumes_${user.username}`);
        if (savedSelected) {
          setSelectedResumes(JSON.parse(savedSelected));
        }
      });

      fetchResumeSelections(user.username).then(setSelectedResumes);
    }
  }, []);

  useEffect(() => {
    if (userInfo) {
      localStorage.setItem(`selectedResumes_${userInfo.username}`, JSON.stringify(selectedResumes));
      saveResumeSelections(userInfo.username, selectedResumes);
    }
  }, [selectedResumes, userInfo]);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <CssBaseline />
      <Header userInfo={userInfo} />
      <Box component="main" sx={{ flexGrow: 1, mt: 10, px: 2 }}>
        <Container maxWidth="md">
          <Stack spacing={4}>
            <Typography variant="h4" textAlign="center" gutterBottom fontWeight={600}>
              Resume & Cover Letter Generator
            </Typography>
            <FileUpload
              userInfo={userInfo}
              uploadedResumes={uploadedResumes}
              setUploadedResumes={setUploadedResumes}
              selectedResumes={selectedResumes}
              setSelectedResumes={setSelectedResumes}
              regenLoading={regenLoading}
              setRegenLoading={setRegenLoading}
              regenMessage={regenMessage}
              setRegenMessage={setRegenMessage}
            />
            <InputForm
              jobLink={jobLink}
              setJobLink={setJobLink}
              jobText={jobText}
              setJobText={setJobText}
              userInfo={userInfo}
              setResume={setResume}
              setCoverLetter={setCoverLetter}
              loading={loading}
              setLoading={setLoading}
            />
            <OutputTabs resume={resume} coverLetter={coverLetter} />
          </Stack>
        </Container>
      </Box>
      <Footer />
    </Box>
  );
};

export default ResumeGenerator;