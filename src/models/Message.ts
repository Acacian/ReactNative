export class Message {
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;

  constructor(content: string, sender: 'user' | 'bot') {
    this.content = content;
    this.sender = sender;
    this.timestamp = new Date();
  }

  getFormattedTimestamp(): string {
    return this.timestamp.toLocaleTimeString();
  }
}