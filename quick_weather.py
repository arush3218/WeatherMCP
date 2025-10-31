from weather import get_current_weather

result = get_current_weather('bangalore')
print(f"🌤️  {result['city']}: {result['temperature']}{result['unit']}")
print(f"📅 Time: {result['time']}")
print(f"🌍 Timezone: {result['timezone']}")
