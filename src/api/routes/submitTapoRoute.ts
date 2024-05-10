import express from "express";
import { cloudLogin, loginDeviceByIp } from "tp-link-tapo-connect";

const router = express.Router();
router.post("/api/tapoControl", async (req, res) => {
    const { email, password, deviceIp, address } = req.body;
    console.log(req.body,'request body ______________________')
    // Hardcoded email and password for testing
    // const email = "saf7001@gmail.com";
    // const password = "JCS68117";
    // const deviceIp = "192.168.0.16"; // Hardcoded device IP address for testing
    // const deviceIp = "Y236070008160";
    // const deviceIp = "saf7001@gmail.com";

    try {
        // Login to TP-Link Cloud API
        const cloudApi = await cloudLogin(email, password);

        // List devices by type (SMART.TAPOPLUG)
        const devices = await cloudApi.listDevicesByType('SMART.TAPOPLUG');
        console.log(devices,'devices_________________')
        // Assuming you're using the first device in the list
        const device = await loginDeviceByIp(email, password, deviceIp);

        // Get device information
        const getDeviceInfoResponse = await device.getDeviceInfo();
        console.log(getDeviceInfoResponse);

        // Example: Turn on the device
        await device.turnOn();

        // // Example: Set brightness (if applicable)
        // await device.setBrightness(75); // Sets brightness to 75% for smart bulbs only

        // // Example: Turn off the device
        // await device.turnOff();

        res.status(200).send({
            message: "Tapo is working.",
            status: "SUCCESS",
        });
    } catch (error: any) {
        console.error("Error:", error);  // Keep the original message for context
        res.status(500).send({
            message: "Failed to communicate with Tapo device.",
            // message: error,
            status: "ERROR",
        });
    }
});

export default router;
