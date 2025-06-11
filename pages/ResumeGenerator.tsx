import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
  AlignmentType,
  Table,
  TableRow,
  TableCell,
  WidthType,
  BulletList,
  Numbering,
} from 'docx';
import { saveAs } from 'file-saver';


import {
  Box,
  Button,
  Container,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Typography,
  CircularProgress,
  Stack,
  Paper,
  Tabs,
  Tab
  } from '@mui/material';

const BACKEND_URL = 'http://localhost:8000'; // Change as needed

const parseMarkdownToDocx = (markdown: string): (Paragraph | Table)[] => {
  const lines = markdown.split('\n');
  const elements: (Paragraph | Table)[] = [];
  let listItems: string[] = [];
  let numberedItems: string[] = [];
  let inTable = false;
  let tableRows: TableRow[] = [];

  const flushLists = () => {
    if (listItems.length > 0) {
      listItems.forEach(item => {
        elements.push(
          new Paragraph({
            text: item.replace(/^[-*]\s+/, ''),
            bullet: { level: 0 },
          })
        );
      });
      listItems = [];
    }
    if (numberedItems.length > 0) {
      numberedItems.forEach((item, i) => {
        elements.push(
          new Paragraph({
            text: item.replace(/^\d+\.\s+/, ''),
            numbering: {
              reference: 'numbered-list',
              level: 0,
            },
          })
        );
      });
      numberedItems = [];
    }
  };

  lines.forEach(line => {
    const trimmed = line.trim();

    if (trimmed === '') {
      flushLists();
      return;
    }

    // Headings
    if (/^#{1,6}\s/.test(trimmed)) {
      flushLists();
      const level = trimmed.match(/^#+/)![0].length;
      const text = trimmed.replace(/^#+\s*/, '');
      elements.push(
        new Paragraph({
          text,
          heading:
            level === 1
              ? HeadingLevel.HEADING_1
              : level === 2
              ? HeadingLevel.HEADING_2
              : HeadingLevel.HEADING_3,
        })
      );
    }

    // Tables
    else if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      const cells = trimmed
        .slice(1, -1)
        .split('|')
        .map(cell => cell.trim());

      const row = new TableRow({
        children: cells.map(cell =>
          new TableCell({
            children: [new Paragraph(cell)],
            width: { size: 25, type: WidthType.PERCENTAGE },
          })
        ),
      });

      tableRows.push(row);
      inTable = true;
    } else {
      if (inTable) {
        flushLists();
        elements.push(
          new Table({
            rows: tableRows,
            width: { size: 100, type: WidthType.PERCENTAGE },
          })
        );
        tableRows = [];
        inTable = false;
      }

      // Bullet list
      if (/^[-*]\s+/.test(trimmed)) {
        listItems.push(trimmed);
      }
      // Numbered list
      else if (/^\d+\.\s+/.test(trimmed)) {
        numberedItems.push(trimmed);
      }
      // Regular paragraph
      else {
        flushLists();
        elements.push(
          new Paragraph({
            children: parseInlineStyles(trimmed),
          })
        );
      }
    }
  });

  flushLists();

  return elements;
};

// Support inline styles: **bold**, _italic_, __underline__, [link](url)
const parseInlineStyles = (text: string): TextRun[] => {
  const parts: TextRun[] = [];

  const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  let cursor = 0;
  let match: RegExpExecArray | null;

  while ((match = linkRegex.exec(text)) !== null) {
    const [fullMatch, label, url] = match;
    if (match.index > cursor) {
      parts.push(...parseStyles(text.slice(cursor, match.index)));
    }
    parts.push(
      new TextRun({
        text: label,
        style: 'Hyperlink',
        hyperlink: url,
      })
    );
    cursor = match.index + fullMatch.length;
  }

  if (cursor < text.length) {
    parts.push(...parseStyles(text.slice(cursor)));
  }

  return parts;
};

const parseStyles = (text: string): TextRun[] => {
  const patterns: [RegExp, (content: string) => TextRun][] = [
    [/\*\*(.*?)\*\*/g, content => new TextRun({ text: content, bold: true })],
    [/__(.*?)__/g, content => new TextRun({ text: content, underline: {} })],
    [/_([^_]+)_/g, content => new TextRun({ text: content, italics: true })],
  ];

  const result: TextRun[] = [];
  let currentText = text;

  patterns.forEach(([regex, formatter]) => {
    const parts: TextRun[] = [];
    let match: RegExpExecArray | null;
    let lastIndex = 0;

    while ((match = regex.exec(currentText)) !== null) {
      if (match.index > lastIndex) {
        parts.push(new TextRun(currentText.slice(lastIndex, match.index)));
      }
      parts.push(formatter(match[1]));
      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < currentText.length) {
      parts.push(new TextRun(currentText.slice(lastIndex)));
    }

    if (parts.length > 0) {
      currentText = parts.map(p => p.text).join('');
      result.length = 0;
      result.push(...parts);
    }
  });

  if (result.length === 0) {
    return [new TextRun(text)];
  }

  return result;
};

const downloadDocxFile = async (filename: string, content: string) => {
  const elements = parseMarkdownToDocx(content);

  const doc = new Document({
    sections: [
      {
        properties: {},
        children: elements,
      },
    ],
  });

  const blob = await Packer.toBlob(doc);
  saveAs(blob, filename);
};


const ResumeGenerator = () => {
  const [users, setUsers] = useState<string[]>([]);
  const [selectedUser, setSelectedUser] = useState('');
  const [jobLink, setJobLink] = useState('');
  const [jobText, setJobText] = useState('');
  const [resume, setResume] = useState('');
  const [coverLetter, setCoverLetter] = useState('');
  const [loading, setLoading] = useState(false);

  const [tabIndex, setTabIndex] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabIndex(newValue);
  };

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

  const downloadTextFile = (filename: string, content: string) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };
  
  const handleDownloadResume = () => downloadDocxFile('resume.docx', resume);
  const handleDownloadCover = () => downloadDocxFile('cover_letter.docx', coverLetter);

  console.log(resume)

  return (
    <Container maxWidth="md" sx={{ py: 10 }}>
      <Typography variant="h3" component="h1" align="center" gutterBottom>
        PersoVox Resume Generator
      </Typography>

      <Stack spacing={4}>
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
          <Box mt={10}>
            <Tabs value={tabIndex} onChange={handleTabChange} centered>
              {resume && <Tab label="Resume" />}
              {coverLetter && <Tab label="Cover Letter" />}
            </Tabs>

            <Box mt={2}>
              {tabIndex === 0 && resume && (
                <>
                  <Typography variant="h5" gutterBottom>
                    Generated Resume
                  </Typography>
                  <Paper
                    variant="outlined"
                    sx={{
                      p: 3,
                      bgcolor: 'grey.100',
                      maxHeight: 500,
                      overflowY: 'auto',
                      fontFamily: 'inherit',
                      whiteSpace: 'normal',
                      fontSize: '1rem',
                      lineHeight: 1.6,
                    }}
                  >
                    <ReactMarkdown remarkPlugins={[remarkGfm]} >
                      {resume}
                    </ReactMarkdown>
                  </Paper>
                  <Box mt={2}>
                  <Button
                    variant="outlined"
                    onClick={handleDownloadResume}
                  >
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
                  <Paper
                    variant="outlined"
                    sx={{
                      p: 3,
                      bgcolor: 'grey.100',
                      maxHeight: 500,
                      overflowY: 'auto',
                      fontFamily: 'inherit',
                      whiteSpace: 'normal',
                      fontSize: '1rem',
                      lineHeight: 1.6,
                    }}
                  >
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {coverLetter}
                    </ReactMarkdown>
                  </Paper>
                  <Box mt={2}>
                    <Button
                      variant="outlined"
                      onClick={handleDownloadCover}
                    >
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
  );
};

export default ResumeGenerator;
