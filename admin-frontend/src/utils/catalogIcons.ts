import { 
  Wrench, 
  Zap, 
  Sparkles, 
  Scissors, 
  Hammer, 
  Paintbrush, 
  Snowflake, 
  Bug, 
  Home, 
  Car, 
  Flame, 
  Tv, 
  Shirt, 
  HeartHandshake, 
  FolderTree, 
  Droplet
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

export const getCategoryIcon = (name: string): LucideIcon => {
  const lower = name.toLowerCase();

  if (lower.includes('plumb') || lower.includes('pipe') || lower.includes('tap') || lower.includes('water')) return Wrench;
  if (lower.includes('electric') || lower.includes('wir') || lower.includes('zap') || lower.includes('power')) return Zap;
  if (lower.includes('clean') || lower.includes('sanitize') || lower.includes('mop') || lower.includes('maid')) return Sparkles;
  if (lower.includes('beauty') || lower.includes('salon') || lower.includes('hair') || lower.includes('spa') || lower.includes('groom')) return Scissors;
  if (lower.includes('carpent') || lower.includes('furnit') || lower.includes('wood')) return Hammer;
  if (lower.includes('paint') || lower.includes('wall') || lower.includes('decor')) return Paintbrush;
  if (lower.includes('ac') || lower.includes('cool') || lower.includes('air cond') || lower.includes('freez')) return Snowflake;
  if (lower.includes('appliance') || lower.includes('repair') || lower.includes('tv') || lower.includes('wash')) return Tv;
  if (lower.includes('pest') || lower.includes('bug') || lower.includes('termite') || lower.includes('insect')) return Bug;
  if (lower.includes('reno') || lower.includes('home') || lower.includes('build') || lower.includes('decor')) return Home;
  if (lower.includes('car') || lower.includes('auto') || lower.includes('bike') || lower.includes('vehic')) return Car;
  if (lower.includes('gas') || lower.includes('stove') || lower.includes('kitchen') || lower.includes('cook')) return Flame;
  if (lower.includes('laundry') || lower.includes('cloth') || lower.includes('iron')) return Shirt;
  if (lower.includes('care') || lower.includes('health') || lower.includes('nurs')) return HeartHandshake;
  if (lower.includes('water') || lower.includes('ro') || lower.includes('purif')) return Droplet;

  return FolderTree;
};

export const getServiceIcon = (name: string, category: string = ''): LucideIcon => {
  const lower = (name + ' ' + category).toLowerCase();

  if (lower.includes('cut') || lower.includes('trim') || lower.includes('salon') || lower.includes('style')) return Scissors;
  if (lower.includes('leak') || lower.includes('pipe') || lower.includes('plumb') || lower.includes('drain')) return Wrench;
  if (lower.includes('wire') || lower.includes('switch') || lower.includes('circuit') || lower.includes('socket')) return Zap;
  if (lower.includes('deep') || lower.includes('sanitize') || lower.includes('clean') || lower.includes('wash')) return Sparkles;
  if (lower.includes('paint') || lower.includes('touchup') || lower.includes('color')) return Paintbrush;
  if (lower.includes('gas') || lower.includes('flame') || lower.includes('stove')) return Flame;
  if (lower.includes('tv') || lower.includes('mount') || lower.includes('screen')) return Tv;
  if (lower.includes('ac') || lower.includes('cool') || lower.includes('snow')) return Snowflake;

  return getCategoryIcon(name);
};
