export interface Device {
  id: { toString: () => any; };
   mac: string;
   latitude: string; 
   longitude: string; 
   name: string;
}
