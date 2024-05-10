import axios from "axios";
import express from "express";

const router = express.Router();

const switchBotApiBaseUrl = 'https://api.switch-bot.com/v1.0';

router.post('/api/submitSwitchBotAction', async (req: any, res: any) => {
  try {
    const { token, deviceId, command } = req.body;

    if (!token || !deviceId || !command) {
      return res.status(400).send('Missing required parameters');
    }

    const apiUrl = `${switchBotApiBaseUrl}/devices/${deviceId}/commands`;

    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };

    const requestBody = {
      command: command,
      parameter: 'default',
      commandType: 'command',
    };

    // Make POST request to send command to the specified device
    const response = await axios.post(apiUrl, requestBody, { headers });

    console.log('SwitchBot Command Response:', response.data);

    if (response.status === 200 && response.data.statusCode === 100 && response.data.message === 'success') {
      res.status(200).json({
        statusCode: 100,
        body: response.data.body,
        message: 'Successfully Communicated with Switcbot API'
      });
    } else {
      res.status(500).send('Internal Server Error');
    }
    
  } catch (error) {
    console.error('Error sending command:', error);
    res.status(500).send('Internal Server Error');
  }
});

export default router;


