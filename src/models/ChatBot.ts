import { useState, useRef } from 'react';
import { FlatList, StyleSheet } from 'react-native';
import ChatInput from '../components/ChatInput';
import ChatMessage from '../components/ChatMessage';
import Header from '../components/Header';
import Footer from '../components/Footer';
import AIEngine from '../models/AIEngine';

const useChatbot = () => {
  const [messages, setMessages] = useState<Array<{ id: string; text: string; isBot: boolean }>>([]);
  const aiEngine = useRef(new AIEngine()).current;

  const handleSendMessage = async (text: string) => {
    const userMessage = { id: Date.now().toString(), text, isBot: false };
    setMessages(prevMessages => [...prevMessages, userMessage]);

    try {
      const response = await aiEngine.sendMessage(text);
      const botMessage = { id: (Date.now() + 1).toString(), text: response, isBot: true };
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error getting AI response:', error);
      const errorMessage = { id: (Date.now() + 1).toString(), text: 'Sorry, an error occurred.', isBot: true };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    }
  };

  return {
    messages,
    handleSendMessage,
  };
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  chatContainer: {
    flex: 1,
    justifyContent: 'flex-end',
  },
  messageList: {
    flex: 1,
    padding: 10,
  },
});

export { useChatbot, styles };
