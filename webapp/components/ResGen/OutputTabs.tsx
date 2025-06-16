import React, { useState } from 'react';
import { Box, Tabs, Tab, Typography, Paper, Button } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { downloadDocxFile } from '../../utils/api';

interface OutputTabsProps {
  resume: string;
  coverLetter: string;
}

const OutputTabs: React.FC<OutputTabsProps> = ({ resume, coverLetter }) => {
  const [tabIndex, setTabIndex] = useState(0);

  return (
    <>
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
    </>
  );
};

export default OutputTabs;