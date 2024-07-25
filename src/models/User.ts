import { UserPreferences } from './UserPreferences';

export class User {
  name: string;
  age: number;
  preferences: UserPreferences;

  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
    this.preferences = new UserPreferences();
  }

  updateName(newName: string) {
    this.name = newName;
  }

  updateAge(newAge: number) {
    this.age = newAge;
  }

  addPreference(like: string) {
    this.preferences.addLike(like);
  }

  addDislike(dislike: string) {
    this.preferences.addDislike(dislike);
  }

  addToHistory(message: string) {
    this.preferences.addToHistory(message);
  }
}