export type Predicate =
  | "is-a"
  | "thuoc-the-ky"
  | "doi-dau-voi"
  | "noi-tieng-voi"
  | "gan-voi-dia-danh"
  | "co-tac-pham"
  | "gioi-tinh"
  | "sang-lap";

export interface Triple {
  s: string;
  p: Predicate;
  o: string;
}

export interface Entity {
  id: string;
  name: string;
  alias?: string[];
}

export type Answer = "yes" | "no" | "unsure";

export interface Feature {
  id: string;
  question: string;
  holds: (entityId: string) => boolean;
}

export interface Turn {
  question: string;
  featureId: string;
  answer: Answer;
  informationGain: number;
  entropyAfter: number;
}

export interface GameState {
  posterior: Record<string, number>;
  askedFeatureIds: string[];
  turns: Turn[];
}
