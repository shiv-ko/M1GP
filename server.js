const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

const statusFilePath = path.join(__dirname, 'public', 'status.json');

app.get('/status', (req, res) => {
  fs.readFile(statusFilePath, 'utf8', (err, data) => {
    if (err) {
      res.status(500).send('Error reading status file');
      return;
    }
    res.send(JSON.parse(data));
  });
});

app.post('/status', (req, res) => {
  const newStatus = req.body;
  fs.writeFile(statusFilePath, JSON.stringify(newStatus, null, 2), 'utf8', (err) => {
    if (err) {
      res.status(500).send('Error writing to status file');
      return;
    }
    res.send(newStatus);
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
