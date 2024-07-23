import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const Footer = () => (
  <View style={styles.footer}>
    <Text>Footer</Text>
  </View>
);

const styles = StyleSheet.create({
  footer: {
    backgroundColor: 'lightgreen',
    padding: 10,
  },
});

export default Footer;