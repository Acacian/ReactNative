import { AppRegistry } from 'react-native';
import App from './src/App.tsx';  // .tsx 확장자 추가
import { name as appName } from './app.json';
import { render } from 'react-dom';

AppRegistry.registerComponent(appName, () => App);

const rootTag = document.getElementById('root') || document.getElementById('main');
AppRegistry.runApplication(appName, { initialProps: {}, rootTag });
