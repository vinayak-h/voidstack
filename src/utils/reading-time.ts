const WORDS_PER_MINUTE = 200;

export interface ReadingStats {
  words: number;
  minutes: number;
}

export function getReadingStats(body: string): ReadingStats {
  const words = body.trim().split(/\s+/).filter(Boolean).length;
  const minutes = Math.max(1, Math.round(words / WORDS_PER_MINUTE));
  return { words, minutes };
}
