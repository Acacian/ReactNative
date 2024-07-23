import axios from 'axios';

class AIEngine {
  private baseURL: string;

  constructor() {
    this.baseURL = 'http://172.17.0.1:5000'; // Docker host IP
  }

  async sendMessage(message: string): Promise<string> {
    try {
      const response = await axios.post(`${this.baseURL}/chat`, { message });
      return response.data.response;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }
}

export default AIEngine;