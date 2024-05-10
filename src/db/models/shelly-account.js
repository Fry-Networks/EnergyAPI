import mongoose from "mongoose";

const ShellyAccountSchema = new mongoose.Schema({
  message: String,
    walletaddress: String,
    serverUrl: String,
    deviceId: String,
    authKey: String,
    data: {
        isok: Boolean,
        device_status: {
            id: String,
            _updated: String,
            serial: Number,
            sys: {
                available_updates: {
                    stable: {
                        version: String
                    }
                },
                mac: String,
                restart_required: Boolean,
                time: String,
                unixtime: Number,
                uptime: Number,
                ram_size: Number,
                ram_free: Number,
                fs_size: Number,
                fs_free: Number,
                cfg_rev: Number,
                kvs_rev: Number,
                schedule_rev: Number,
                webhook_rev: Number,
                reset_reason: Number
            },
            cloud: {
                connected: Boolean
            },
            wifi: {
                sta_ip: String,
                status: String,
                ssid: String,
                rssi: Number
            },
            mqtt: {
                connected: Boolean
            },
            ble: Array,
            ws: {
                connected: Boolean
            },
            "switch:0": {
                id: Number,
                aenergy: {
                    by_minute: Array,
                    minute_ts: Number,
                    total: Number
                },
                source: String,
                output: Boolean,
                apower: Number,
                voltage: Number,
                current: Number,
                temperature: {
                    tC: Number,
                    tF: Number
                }
            },
            code: String
        }
    },
    status: String,
    metadata: {
        data_type: String
    }
});

// Define the model for storing latest data
export const ShellyAccountModel = mongoose.model("ShellyAccount", ShellyAccountSchema);

// Define schema for storing historical data with timestamps
const ShellySchema = new mongoose.Schema({
  device_status: {
    id: String,
    _updated: String,
    serial: Number,
    sys: {
      available_updates: {
        stable: {
          version: String
        }
      },
      mac: String,
      restart_required: Boolean,
      time: String,
      unixtime: Number,
      uptime: Number,
      ram_size: Number,
      ram_free: Number,
      fs_size: Number,
      fs_free: Number,
      cfg_rev: Number,
      kvs_rev: Number,
      schedule_rev: Number,
      webhook_rev: Number,
      reset_reason: Number
    },
    cloud: {
      connected: Boolean
    },
    wifi: {
      sta_ip: String,
      status: String,
      ssid: String,
      rssi: Number
    },
    mqtt: {
      connected: Boolean
    },
    ble: Array,
    ws: {
      connected: Boolean
    },
    "switch:0": {
      id: Number,
      aenergy: {
        by_minute: Array,
        minute_ts: Number,
        total: Number
      },
      source: String,
      output: Boolean,
      apower: Number,
      voltage: Number,
      current: Number,
      temperature: {
        tC: Number,
        tF: Number
      }
    },
    code: String
  },
  timestamp: { type: Date, default: Date.now },
  metadata: {
    data_type: String,
    deviceId: String
  }
});

// Define the model for storing historical data
export const Shelly = mongoose.model("Shelly", ShellySchema);
