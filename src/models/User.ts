export interface UserPreferences {
    likes: string[];
    dislikes: string[];
    history: string[];
  }
  
  export class User {
    name: string;
    age: number;
    preferences: UserPreferences;
  
    constructor(name: string, age: number) {
      this.name = name;
      this.age = age;
      this.preferences = { likes: [], dislikes: [], history: [] };
    }
  
    addPreference(like: string) {
      this.preferences.likes.push(like);
    }
  
    addDislike(dislike: string) {
      this.preferences.dislikes.push(dislike);
    }
  
    addToHistory(message: string) {
      this.preferences.history.push(message);
    }
  }
  