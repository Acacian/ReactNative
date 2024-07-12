export class Message {
    content: string;
    sender: 'user' | 'bot';
  
    constructor(content: string, sender: 'user' | 'bot') {
      this.content = content;
      this.sender = sender;
    }
  }
  