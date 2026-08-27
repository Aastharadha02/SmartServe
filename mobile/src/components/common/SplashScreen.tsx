import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Dimensions,
  Easing,
} from 'react-native';
import Svg, { Path, Rect } from 'react-native-svg';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

const AnimatedPath = Animated.createAnimatedComponent(Path);
const AnimatedRect = Animated.createAnimatedComponent(Rect);

interface SplashScreenProps {
  onAnimationComplete: () => void;
}

export const SplashScreen: React.FC<SplashScreenProps> = ({ onAnimationComplete }) => {
  // S path drawing animation
  const sProgress = useRef(new Animated.Value(0)).current;
  // Square border drawing animation
  const sqProgress = useRef(new Animated.Value(0)).current;
  // Wordmark & tagline fade in
  const textOpacity = useRef(new Animated.Value(0)).current;
  const textTranslateY = useRef(new Animated.Value(8)).current;
  // Full container handoff exit
  const containerOpacity = useRef(new Animated.Value(1)).current;
  const logoScale = useRef(new Animated.Value(1)).current;
  const logoTranslateY = useRef(new Animated.Value(0)).current;

  // Path lengths
  const S_PATH_LENGTH = 160;
  const SQ_PATH_LENGTH = 320;

  useEffect(() => {
    // 1. Hand-sketched S stroke drawing (1200ms)
    Animated.sequence([
      Animated.timing(sProgress, {
        toValue: 1,
        duration: 1200,
        easing: Easing.bezier(0.25, 0.1, 0.25, 1.0),
        useNativeDriver: false,
      }),
      // 2. Hand-sketched square frame drawing (700ms)
      Animated.timing(sqProgress, {
        toValue: 1,
        duration: 700,
        easing: Easing.bezier(0.25, 0.1, 0.25, 1.0),
        useNativeDriver: false,
      }),
      // 3. Wordmark & Tagline appearance (600ms)
      Animated.parallel([
        Animated.timing(textOpacity, {
          toValue: 1,
          duration: 600,
          easing: Easing.out(Easing.quad),
          useNativeDriver: true,
        }),
        Animated.timing(textTranslateY, {
          toValue: 0,
          duration: 600,
          easing: Easing.out(Easing.quad),
          useNativeDriver: true,
        }),
      ]),
      // 4. Final hold (500ms)
      Animated.delay(500),
      // 5. Logo handoff translation & fade (650ms)
      Animated.parallel([
        Animated.timing(logoTranslateY, {
          toValue: -80,
          duration: 650,
          easing: Easing.bezier(0.4, 0.0, 0.2, 1),
          useNativeDriver: true,
        }),
        Animated.timing(logoScale, {
          toValue: 0.85,
          duration: 650,
          easing: Easing.bezier(0.4, 0.0, 0.2, 1),
          useNativeDriver: true,
        }),
        Animated.timing(containerOpacity, {
          toValue: 0,
          duration: 650,
          easing: Easing.inOut(Easing.quad),
          useNativeDriver: true,
        }),
      ]),
    ]).start(() => {
      onAnimationComplete();
    });
  }, []);

  const sDashOffset = sProgress.interpolate({
    inputRange: [0, 1],
    outputRange: [S_PATH_LENGTH, 0],
  });

  const sqDashOffset = sqProgress.interpolate({
    inputRange: [0, 1],
    outputRange: [SQ_PATH_LENGTH, 0],
  });

  return (
    <Animated.View style={[styles.container, { opacity: containerOpacity }]}>
      <Animated.View
        style={[
          styles.logoContainer,
          {
            transform: [
              { translateY: logoTranslateY },
              { scale: logoScale },
            ],
          },
        ]}
      >
        {/* Vector SVG Brand Icon */}
        <View style={styles.svgWrapper}>
          <Svg width={96} height={96} viewBox="0 0 96 96">
            {/* Square outer frame */}
            <AnimatedRect
              x={6}
              y={6}
              width={84}
              height={84}
              rx={18}
              stroke="#2563EB"
              strokeWidth={4.5}
              fill="none"
              strokeDasharray={SQ_PATH_LENGTH}
              strokeDashoffset={sqDashOffset}
            />
            {/* Hand-sketched S curve */}
            <AnimatedPath
              d="M 62 30 C 62 23, 34 22, 34 38 C 34 54, 62 48, 62 64 C 62 80, 34 78, 34 70"
              stroke="#0F172A"
              strokeWidth={7}
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
              strokeDasharray={S_PATH_LENGTH}
              strokeDashoffset={sDashOffset}
            />
          </Svg>
        </View>

        {/* Wordmark & Tagline */}
        <Animated.View
          style={[
            styles.textContainer,
            {
              opacity: textOpacity,
              transform: [{ translateY: textTranslateY }],
            },
          ]}
        >
          <View style={styles.wordmarkRow}>
            <Text style={styles.brandSmart}>Smart</Text>
            <Text style={styles.brandServe}>Serve</Text>
          </View>
          <Text style={styles.tagline}>Smart Service Booking & Management</Text>
        </Animated.View>
      </Animated.View>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFill,
    backgroundColor: '#FAF9F5',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 9999,
  },
  logoContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  svgWrapper: {
    width: 96,
    height: 96,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 20,
  },
  textContainer: {
    alignItems: 'center',
  },
  wordmarkRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginBottom: 6,
  },
  brandSmart: {
    fontSize: 28,
    fontWeight: '800',
    color: '#0F172A',
    letterSpacing: -0.5,
  },
  brandServe: {
    fontSize: 28,
    fontWeight: '800',
    color: '#2563EB',
    letterSpacing: -0.5,
  },
  tagline: {
    fontSize: 13,
    fontWeight: '500',
    color: '#64748B',
    letterSpacing: 0.2,
  },
});
