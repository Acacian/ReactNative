export class UserPreferences {
  likes: Set<string>;
  dislikes: Set<string>;
  history: string[];
  maxHistoryLength: number;

  constructor(maxHistoryLength: number = 100) {
    this.likes = new Set();
    this.dislikes = new Set();
    this.history = [];
    this.maxHistoryLength = maxHistoryLength;
  }

  addLike(like: string) {
    this.likes.add(like);
    this.dislikes.delete(like);  // Remove from dislikes if present
  }

  addDislike(dislike: string) {
    this.dislikes.add(dislike);
    this.likes.delete(dislike);  // Remove from likes if present
  }

  addToHistory(message: string) {
    this.history.push(message);
    if (this.history.length > this.maxHistoryLength) {
      this.history.shift();
    }
  }

  getRecentHistory(n: number): string[] {
    return this.history.slice(-n);
  }
}