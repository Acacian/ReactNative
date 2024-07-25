export class ScenarioManager {
  private currentScenario: string;
  private scenarios: Record<string, (input: string) => string>;

  constructor() {
    this.currentScenario = 'default';
    this.scenarios = {
      default: (input: string) => `Default response to: ${input}`,
      greeting: (input: string) => `Hello! How can I help you today?`,
      farewell: (input: string) => `Goodbye! Have a great day!`,
    };
  }

  switchScenario(scenario: string) {
    if (this.scenarios[scenario]) {
      this.currentScenario = scenario;
    } else {
      console.warn(`Scenario ${scenario} not found. Staying on current scenario.`);
    }
  }

  getCurrentScenario(): string {
    return this.currentScenario;
  }

  getResponse(input: string): string {
    return this.scenarios[this.currentScenario](input);
  }

  addScenario(name: string, handler: (input: string) => string) {
    this.scenarios[name] = handler;
  }
}