import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Dimensions } from 'react-native';
import ChatInput from '../components/ChatInput';
import ChatMessage from '../components/ChatMessage';
import Header from '../components/Header';
import Footer from '../components/Footer';

const ChatbotScreen = () => {
  const [messages, setMessages] = useState<Array<{ id: string; text: string; isBot: boolean }>>([]);

  const handleSendMessage = (text: string) => {
    setMessages(prevMessages => [
      ...prevMessages,
      { id: Date.now().toString(), text, isBot: false },
      { id: (Date.now() + 1).toString(), text: `Echo: ${text}`, isBot: true }
    ]);
  };

  return (
    <View style={styles.container}>
      <Header />
      <ScrollView style={styles.chatContainer}>
        {messages.map(message => (
          <ChatMessage key={message.id} message={message.text} isBot={message.isBot} />
        ))}
      </ScrollView>
      <ChatInput onSendMessage={handleSendMessage} />
      <Footer />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    height: Dimensions.get('window').height,
  },
  chatContainer: {
    flex: 1,
    padding: 10,
  },
});

export default ChatbotScreen;