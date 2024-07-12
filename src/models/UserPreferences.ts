export class UserPreferences {
    likes: string[];
    dislikes: string[];
    history: string[];
  
    constructor() {
      this.likes = [];
      this.dislikes = [];
      this.history = [];
    }
  
    addLike(like: string) {
      this.likes.push(like);
    }
  
    addDislike(dislike: string) {
      this.dislikes.push(dislike);
    }
  
    addToHistory(message: string) {
      this.history.push(message);
    }
  }
  