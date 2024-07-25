import { Message } from './Message';

export class Conversation {
  messages: Message[];
  maxHistory: number;

  constructor(maxHistory: number = 50) {
    this.messages = [];
    this.maxHistory = maxHistory;
  }

  addMessage(message: Message) {
    this.messages.push(message);
    if (this.messages.length > this.maxHistory) {
      this.messages.shift();
    }
  }

  getMessages(): Message[] {
    return this.messages;
  }

  getLastNMessages(n: number): Message[] {
    return this.messages.slice(-n);
  }
}