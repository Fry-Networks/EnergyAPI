import mongoose from "mongoose";

const ecowittAccountSchema = new mongoose.Schema({
  user_id: mongoose.Schema.Types.ObjectId,
  timestamp: Date,
  api_type: String,
  walletAddress: String,
  devices: {
    type: [
      {
        id: { type: String, required: false },
        deviceMAC: String,
        date_zone_id: String,
        infos: {
          coords: {
            lat: Number,
            lon: Number,
          },
          name: String,
        },
      },
    ],
    default: [],
  },
});

const deviceSchema = new mongoose.Schema({
  id: { type: Number, required: true },
  name: String,
  mac: String,
  type: Number,
  date_zone_id: String,
  createtime: Number,
  longitude: Number,
  latitude: Number,
  stationtype: String,
});

const EcowittSchema = new mongoose.Schema({
  timestamp: Date,
  devices: {
    type: [
      {
        id: { type: String, required: false },
        deviceMAC: String,
        date_zone_id: String,
        infos: {
          coords: {
            lat: Number,
            lon: Number,
          },
          name: String,
        },
      },
    ],
    default: [],
  },
  timestamp: { type: Date, default: Date.now },
  metadata: {
    data_type: String,
  }
});

const EcowittaccountSchema = new mongoose.Schema({
  api_key: { type: String, required: true },
  app_key: { type: String, required: true },
  devices: [deviceSchema]
});

const EcowittAccount = mongoose.model('ecowitt-Accounts', ecowittAccountSchema);

// Define the model for storing historical data
export const Ecowitt = mongoose.model("Ecowitt", EcowittSchema);

export const Ecowittmodel = EcowittAccount.discriminator('Ecowittaccount', EcowittaccountSchema);
