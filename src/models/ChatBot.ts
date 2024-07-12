import { AIEngine } from './AIEngine';
import { Message } from './Message';

export class ChatBot {
  aiEngine: AIEngine;

  constructor(aiEngine: AIEngine) {
    this.aiEngine = aiEngine;
  }

  respondTo(message: string): Message {
    const response = this.aiEngine.generateResponse(message);
    return new Message(response, 'bot');
  }
}
