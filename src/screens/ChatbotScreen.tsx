import React, { useState, useRef } from 'react';
import { View, FlatList, StyleSheet, SafeAreaView } from 'react-native';
import ChatInput from '../components/ChatInput';
import ChatMessage from '../components/ChatMessage';
import Header from '../components/Header';
import Footer from '../components/Footer';
import AIEngine from '../models/AIEngine';

const ChatbotScreen = () => {
  const [messages, setMessages] = useState<Array<{ id: string; text: string; isBot: boolean }>>([]);
  const aiEngine = useRef(new AIEngine()).current;

  const handleSendMessage = async (text: string) => {
    setMessages(prevMessages => [...prevMessages, { id: Date.now().toString(), text, isBot: false }]);

    try {
      const response = await aiEngine.sendMessage(text);
      setMessages(prevMessages => [...prevMessages, { id: (Date.now() + 1).toString(), text: response, isBot: true }]);
    } catch (error) {
      console.error('Error getting AI response:', error);
      setMessages(prevMessages => [...prevMessages, { id: (Date.now() + 1).toString(), text: 'Sorry, an error occurred.', isBot: true }]);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <Header />
      <FlatList
        data={messages}
        renderItem={({ item }) => <ChatMessage message={item.text} isBot={item.isBot} />}
        keyExtractor={item => item.id}
        style={styles.messageList}
      />
      <ChatInput onSendMessage={handleSendMessage} />
      <Footer />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  messageList: {
    flex: 1,
    padding: 10,
  },
});

export default ChatbotScreen;