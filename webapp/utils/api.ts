import axios from 'axios';
import { saveAs } from 'file-saver';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const fetchResumes = async (username: string): Promise<string[]> => {
  try {
    const res = await axios.get(`${BACKEND_URL}/list_resumes`, {
      params: { username },
    });
    return res.data.resumes;
  } catch (err) {
    console.error('Failed to fetch uploaded resumes', err);
    return [];
  }
};

export const fetchResumeSelections = async (username: string): Promise<string[]> => {
  try {
    const res = await axios.get(`${BACKEND_URL}/get_resume_selections`, {
      params: { username },
    });
    return res.data;
  } catch (err) {
    console.error('Failed to load selected resumes from backend', err);
    return [];
  }
};

export const saveResumeSelections = async (username: string, selectedResumes: string[]) => {
  try {
    await axios.post(`${BACKEND_URL}/save_resume_selections`, {
      username,
      selected_resumes: selectedResumes,
    });
  } catch (err) {
    console.error('Failed to save resume selections', err);
  }
};

export const generateResume = async (username: string, jobLink: string, jobText: string) => {
  const response = await axios.post(`${BACKEND_URL}/generate`, {
    user: username,
    job_link: jobLink,
    job_text: jobText,
  });
  return response.data;
};

export const regenerateKnowledgeBase = async (username: string, selectedResumes: string[]) => {
  const response = await axios.post(`${BACKEND_URL}/regenerate_knowledgebase`, {
    username,
    selected_resumes: selectedResumes,
  });
  return response.data.message || 'Knowledge base regenerated successfully.';
};

export const downloadResume = async (username: string, filename: string) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/download_resume`, {
      params: { username, filename },
      responseType: 'blob',
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.parentNode?.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error downloading resume:', error);
    alert('Failed to download the resume.');
  }
};

export const deleteResume = async (username: string, filename: string) => {
  const response = await axios.delete(`${BACKEND_URL}/delete_resume`, {
    data: { username, filename },
  });
  return response.data.message || `"${filename}" deleted.`;
};

export const uploadResume = async (username: string, file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(
    `${BACKEND_URL}/upload_resume?username=${encodeURIComponent(username)}`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );
  return response.data.message;
};

export const downloadDocxFile = (filename: string, content: string) => {
  const blob = new Blob([content], {
    type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  });
  saveAs(blob, filename);
};