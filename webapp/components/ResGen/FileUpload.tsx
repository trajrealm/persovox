import React, { useRef } from 'react';
import {
  Box,
  Button,
  Typography,
  IconButton,
  CircularProgress,
  Input,
} from '@mui/material';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DownloadIcon from '@mui/icons-material/Download';
import DeleteIcon from '@mui/icons-material/Delete';
import { downloadResume, deleteResume, uploadResume, regenerateKnowledgeBase } from '../../utils/api';

interface FileUploadProps {
  userInfo: { username: string; email: string } | null;
  uploadedResumes: string[];
  setUploadedResumes: React.Dispatch<React.SetStateAction<string[]>>;
  selectedResumes: string[];
  setSelectedResumes: React.Dispatch<React.SetStateAction<string[]>>;
  regenLoading: boolean;
  setRegenLoading: React.Dispatch<React.SetStateAction<boolean>>;
  regenMessage: string;
  setRegenMessage: React.Dispatch<React.SetStateAction<string>>;
}

const FileUpload: React.FC<FileUploadProps> = ({
  userInfo,
  uploadedResumes,
  setUploadedResumes,
  selectedResumes,
  setSelectedResumes,
  regenLoading,
  setRegenLoading,
  regenMessage,
  setRegenMessage,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const toggleResumeSelection = (filename: string) => {
    setSelectedResumes(prev =>
      prev.includes(filename)
        ? prev.filter(f => f !== filename)
        : [...prev, filename]
    );
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !userInfo) return;

    try {
      await uploadResume(userInfo.username, file);
      const resumes = await (await import('../../utils/api')).fetchResumes(userInfo.username);
      setUploadedResumes(resumes);
    } catch (err) {
      console.error(err);
      alert('Error uploading file.');
    }
  };

  const handleRegenerate = async () => {
    if (!userInfo || selectedResumes.length === 0) {
      alert('Please select at least one resume to regenerate knowledge base.');
      return;
    }
    try {
      setRegenLoading(true);
      const message = await regenerateKnowledgeBase(userInfo.username, selectedResumes);
      setRegenMessage(message);
    } catch (error) {
      console.error(error);
      setRegenMessage('Failed to regenerate knowledge base.');
    } finally {
      setRegenLoading(false);
    }
  };

  const handleDelete = async (filename: string) => {
    if (!userInfo || !window.confirm(`Are you sure you want to delete "${filename}"?`)) return;
    try {
      await deleteResume(userInfo.username, filename);
      const resumes = await (await import('../../utils/api')).fetchResumes(userInfo.username);
      setUploadedResumes(resumes);
    } catch (error) {
      console.error(error);
      alert('Failed to delete the resume.');
    }
  };

  return (
    <Box sx={{ position: 'relative', mt: 4, mb: 2, px: 2 }}>
      <Box
        sx={{
          border: '1px solid #ccc',
          borderRadius: '8px',
          p: 3,
          pt: 5,
          position: 'relative',
          bgcolor: 'grey.100',
        }}
      >
        <Typography
          sx={{
            position: 'absolute',
            top: '-12px',
            left: 20,
            bgcolor: 'grey.100',
            px: 1,
            fontWeight: 400,
            fontSize: '12px',
          }}
        >
          Upload Your Past Resumes
        </Typography>
        <Button
          variant="outlined"
          startIcon={<UploadFileIcon />}
          onClick={() => fileInputRef.current?.click()}
        >
          Upload Resume (PDF)
        </Button>
        <Input
          type="file"
          inputProps={{ accept: '.pdf,.doc,.docx', multiple: true }}
          sx={{ display: 'none' }}
          inputRef={fileInputRef}
          onChange={handleFileUpload}
        />
        <Box mt={2}>
          {uploadedResumes.length === 0 ? (
            <Typography color="text.secondary">No files uploaded yet.</Typography>
          ) : (
            uploadedResumes.map((file, index) => (
              <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 0.5 }}>
                <input
                  type="checkbox"
                  checked={selectedResumes.includes(file)}
                  onChange={() => toggleResumeSelection(file)}
                  style={{ marginRight: 8 }}
                />
                <PictureAsPdfIcon sx={{ color: '#d32f2f', fontSize: 20, mr: 1 }} />
                <Typography variant="body2" sx={{ flexGrow: 1 }}>
                  {file}
                </Typography>
                <Box>
                  <IconButton
                    aria-label="download"
                    color="primary"
                    onClick={() => downloadResume(userInfo?.username || '', file)}
                    size="small"
                    sx={{ mr: 1 }}
                  >
                    <DownloadIcon />
                  </IconButton>
                  <IconButton
                    aria-label="delete"
                    color="error"
                    onClick={() => handleDelete(file)}
                    size="small"
                  >
                    <DeleteIcon />
                  </IconButton>
                </Box>
              </Box>
            ))
          )}
          <Button
            variant="contained"
            color="primary"
            onClick={handleRegenerate}
            disabled={regenLoading}
            startIcon={regenLoading ? <CircularProgress size={20} /> : null}
            sx={{ mt: 2 }}
          >
            {regenLoading ? 'Refreshing...' : 'Refresh Reference Resumes'}
          </Button>
          {regenMessage && (
            <Typography
              variant="body2"
              color={regenMessage.startsWith('Failed') ? 'error' : 'success'}
              sx={{ mt: 1 }}
            >
              {regenMessage}
            </Typography>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default FileUpload;