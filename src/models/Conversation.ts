import { Message } from './Message';

export class Conversation {
  messages: Message[];

  constructor() {
    this.messages = [];
  }

  addMessage(message: Message) {
    this.messages.push(message);
  }

  getMessages(): Message[] {
    return this.messages;
  }
}
