const express = require('express');
const bodyParser = require('body-parser');
const nodemailer = require('nodemailer');

const app = express();
app.use(bodyParser.json());

// Configure your email service
const transporter = nodemailer.createTransport({
  service: 'outlook',
  auth: {
    user: 'c.bhavya@sonata-software.com',
    pass: 'Varshu@456'
  }
});

// Webhook endpoint to receive payloads
app.post('/webhook', (req, res) => {
  const payload = req.body;

  // Check if it's a closed pull request
  if (payload.action === 'closed') {
    // Construct email content
    const mailOptions = {
      from: 'c.bhavya@sonata-software.com',
      to: 'c.bhavya@sonata-software.com',
      subject: 'Closed Pull Request Notification',
      text: `
        Pull Request #${payload.pull_request.number} in ${payload.repository.full_name} was closed.
        Title: ${payload.pull_request.title}
        URL: ${payload.pull_request.html_url}
      `
    };

    // Send email
    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        console.error('Error sending email:', error);
      } else {
        console.log('Email sent:', info.response);
      }
    });
  }

  res.status(200).end();
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
