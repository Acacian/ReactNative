import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const Footer = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Powered by AI</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    padding: 20,
    backgroundColor: '#6200EE',
    position: 'absolute',
    bottom: 0,
    alignItems: 'center',
  },
  text: {
    color: 'white',
    fontSize: 16,
  },
});

export default Footer;
