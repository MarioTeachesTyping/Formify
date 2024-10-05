const express = require('express');
const { SerialPort } = require('serialport');  // Import SerialPort
const { ReadlineParser } = require('@serialport/parser-readline'); // Import ReadlineParser

const app = express();
const port = 3000;

// Path to the Arduino serial port (update this with the correct port on your machine)
const arduinoPort = 'COM9';  // Replace with the actual port of your Arduino
const baudRate = 9600;               // Ensure this matches the baud rate in your Arduino sketch

// Set up the SerialPort connection to the Arduino
const serialPort = new SerialPort({
  path: arduinoPort,  // Path to the serial port where Arduino is connected
  baudRate: baudRate, // Baud rate
  autoOpen: false     // Open the port manually later
});

// Set up the Readline parser
const parser = serialPort.pipe(new ReadlineParser({ delimiter: '\n' }));

// Serve static files (HTML, CSS, JS) from the 'public' directory
app.use(express.static('public'));

// Open the serial port when the server starts
serialPort.open((err) => {
  if (err) {
    return console.log('Error opening serial port:', err.message);
  }
  console.log('Serial port opened.');
});

// Route to turn the LED on
app.get('/vib/on', (req, res) => {
  console.log('Turning VIB on...');
  serialPort.write('1'); // Send '1' to Arduino to turn the LED on
  res.send('VIB On');
});

// Route to turn the LED off
app.get('/vib/off', (req, res) => {
  console.log('Turning VIB off...');
  serialPort.write('0'); // Send '0' to Arduino to turn the LED off
  res.send('VIB Off');
});

// Read data from Arduino and log it (optional)
parser.on('data', (data) => {
  console.log('Data from Arduino:', data);
});

// Start the Express server on port 3000
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
