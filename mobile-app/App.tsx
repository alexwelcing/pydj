import { StatusBar } from 'expo-status-bar';
import { NavigationContainer, DefaultTheme, Theme } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Text } from 'react-native';
import DashboardScreen from './src/screens/DashboardScreen';
import OpportunitiesScreen from './src/screens/OpportunitiesScreen';
import CaptureScreen from './src/screens/CaptureScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import { colors } from './src/lib/theme';

const Tab = createBottomTabNavigator();

const navTheme: Theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: colors.background,
    card: '#0f1827',
    border: colors.border,
    primary: colors.accent,
    text: colors.text,
    notification: colors.warning,
  },
};

export default function App() {
  return (
    <NavigationContainer theme={navTheme}>
      <StatusBar style="light" />
      <Tab.Navigator
        screenOptions={({ route }) => ({
          headerShown: false,
          tabBarStyle: { backgroundColor: '#0f1827', borderTopColor: colors.border },
          tabBarActiveTintColor: colors.accent,
          tabBarInactiveTintColor: colors.textMuted,
          tabBarIcon: ({ color }) => <Text style={{ color }}>{iconForRoute(route.name)}</Text>,
          tabBarLabelStyle: { fontWeight: '700' },
        })}
      >
        <Tab.Screen name="Dashboard" component={DashboardScreen} />
        <Tab.Screen name="Opportunities" component={OpportunitiesScreen} />
        <Tab.Screen name="Capture" component={CaptureScreen} />
        <Tab.Screen name="Settings" component={SettingsScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

const iconForRoute = (route: string) => {
  switch (route) {
    case 'Dashboard':
      return '📊';
    case 'Opportunities':
      return '🎯';
    case 'Capture':
      return '➕';
    case 'Settings':
      return '⚙️';
    default:
      return '⬜️';
  }
};
