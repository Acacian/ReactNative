export class ScenarioManager {
    currentScenario: string;
  
    constructor() {
      this.currentScenario = 'default';
    }
  
    switchScenario(scenario: string) {
      this.currentScenario = scenario;
    }
  
    getCurrentScenario(): string {
      return this.currentScenario;
    }
  }
  