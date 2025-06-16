import React from 'react';
import { Box, Button, TextField, CircularProgress } from '@mui/material';
import { generateResume } from '../../utils/api';

interface InputFormProps {
  jobLink: string;
  setJobLink: React.Dispatch<React.SetStateAction<string>>;
  jobText: string;
  setJobText: React.Dispatch<React.SetStateAction<string>>;
  userInfo: { username: string; email: string } | null;
  setResume: React.Dispatch<React.SetStateAction<string>>;
  setCoverLetter: React.Dispatch<React.SetStateAction<string>>;
  loading: boolean;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

const InputForm: React.FC<InputFormProps> = ({
  jobLink,
  setJobLink,
  jobText,
  setJobText,
  userInfo,
  setResume,
  setCoverLetter,
  loading,
  setLoading,
}) => {
  const handleGenerate = async () => {
    if (!userInfo) return;
    setLoading(true);
    try {
      const response = await generateResume(userInfo.username, jobLink, jobText);
      setResume(response.resume);
      setCoverLetter(response.cover_letter);
    } catch (err) {
      alert('Error generating resume. Check console.');
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <>
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
        disabled={loading}
        startIcon={loading ? <CircularProgress size={20} /> : null}
        sx={{ alignSelf: 'start' }}
      >
        Generate Resume & Cover Letter
      </Button>
    </>
  );
};

export default InputForm;