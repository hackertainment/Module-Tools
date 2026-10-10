import math
from dataclasses import dataclass
from typing import TypeVar, Generic

@dataclass(frozen=True)
class Person:
	name: str

	def __str__(self) -> str:
		return f"{self.name}"

@dataclass(frozen=True)
class Song:
	artist: Person  # should be a string
	duration: int  # should be an integer in seconds
	title: str  # should be a string

	def __str__(self) -> str:
		return f"{self.artist} - {self.title} ({format_duration(self.duration)})"

@dataclass(frozen=True)
class TalkShow:
	host: Person  # should be a string
	guests: list[Person]  # should be a list of strings
	duration: int  # should be an integer in seconds
	title: str  # should be a string

	def __str__(self) -> str:
		return f"{self.host} - {self.title} ({format_duration(self.duration)}) {format_person(self.guests)}"

@dataclass(frozen=True)
class Podcast(TalkShow):
	sponsor: str

	def __str__(self) -> str:
		return f"{self.host} - {self.title} ({format_duration(self.duration)}) {format_person(self.guests)} <{self.sponsor}>"

T = TypeVar('T', Song, TalkShow)
@dataclass
class Playlist(Generic[T]):
	items: list[T]  # A list of Song or TalkShow or Podcast
	currently_playing_index: int

	def __init__(self, items: list[T]) -> None:
		self.items = items
		self.currently_playing_index = 0

	def __str__(self) -> str:
		return "\n".join(f"{i}. {item}" for i, item in enumerate(self.items))

	def play_next(self) -> None:
		#pass
		# TODO: increment the currently_playing_index, when you get to the end loop back to 0
		self.currently_playing_index = (self.currently_playing_index+1)%len(self.items)

	def get_currently_playing(self) -> str:
		#return "todo"
		# TODO: return a string representation of whatever is playing at the current index
		# See the __str__ method in Song for an example of how to make a string representation of a class
		return str(self.items[self.currently_playing_index])

	def get_total_duration(self) -> int:
		#return 0
		# TODO: return
		total = 0
		for item in self.items:
			total = total + item.duration
		return total

def format_duration(second: int) -> str:
	return "%02d:%02d" % (math.floor(second/60), second%60)

def format_person(persons: list[Person]) -> str:
	return "['" + "', '".join(str(person) for person in persons) + "']"

song_a = Song(Person("Rick Astley"), 210, "Never Gonna Give You Up")
print(song_a)

song_b = Song(Person("Psy"), 219, "Gangnam Style")
funny_songs = Playlist([song_a, song_b])
print()
print(funny_songs)
print("\tTOTAL DURATION", format_duration(funny_songs.get_total_duration()))
print(funny_songs.get_currently_playing())
funny_songs.play_next()
print(funny_songs.get_currently_playing())
funny_songs.play_next()
print(funny_songs.get_currently_playing())

show_a = TalkShow(Person("Melvyn Bragg"), [Person("Jim Al-Khalili"), Person("Sheila Rowan"), Person("Carolin Crawford")], 2700, "Gravitational Waves")
cast_a = Podcast(Person("Steven Strogatz"), [Person("Mary Wootters")], 2340, "How Can Math Protect Our Data", "Simons Foundation")
show_b = TalkShow(Person("Melvyn Bragg"), [Person("Jim Al-Khalili"), Person("Monica Grady"), Person("Ian Stewart")], 2549, "The Physics of Time")
cast_b = Podcast(Person("Janna Levin"), [Person("Thomas Hertog")], 3120, "Why Did The Universe Begin", "Simons Foundation")
show_c = TalkShow(Person("Melvyn Bragg"), [Person("Paul Murdin"), Person("Carolin Crawford"), Person("Ian Crawford")], 2700, "The Moon")
funny_shows = Playlist([show_a, cast_a, show_b, cast_b, show_c])
print()
print(funny_shows)
print("\tTOTAL DURATION", format_duration(funny_shows.get_total_duration()))
print(funny_shows.get_currently_playing())
funny_shows.play_next()
print(funny_shows.get_currently_playing())
funny_shows.play_next()
print(funny_shows.get_currently_playing())
funny_shows.play_next()
print(funny_shows.get_currently_playing())
funny_shows.play_next()
print(funny_shows.get_currently_playing())
funny_shows.play_next()
print(funny_shows.get_currently_playing())
