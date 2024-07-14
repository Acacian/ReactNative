import axios from 'axios';

class AIEngine {
  private baseURL: string;

  constructor() {
    this.baseURL = 'http://172.17.0.1:5000'; // Docker host IP
  }

  async predictIntent(text: string): Promise<string> {
    try {
      const response = await axios.post(`${this.baseURL}/predict`, { text });
      return response.data.intent;
    } catch (error) {
      console.error('Error predicting intent:', error);
      throw error;
    }
  }
}

export default AIEngine;
