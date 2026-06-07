from dataclasses import dataclass, field


@dataclass(frozen=True)
class NavItem:
    slug: str
    label: str
    href: str


@dataclass(frozen=True)
class CalloutSection:
    type: str
    title: str
    body: str


@dataclass(frozen=True)
class GridEntry:
    label: str
    value: str


@dataclass(frozen=True)
class GridSection:
    type: str
    entries: list[GridEntry] = field(default_factory=list)


@dataclass(frozen=True)
class TimelineEntry:
    title: str
    body: str


@dataclass(frozen=True)
class TimelineSection:
    type: str
    entries: list[TimelineEntry] = field(default_factory=list)


@dataclass(frozen=True)
class EventEntry:
    time: str
    title: str
    location: str
    body: str


@dataclass(frozen=True)
class EventSection:
    type: str
    title: str
    entries: list[EventEntry] = field(default_factory=list)


@dataclass(frozen=True)
class LinkEntry:
    label: str
    href: str
    external: bool = False


@dataclass(frozen=True)
class LinkSection:
    type: str
    entries: list[LinkEntry] = field(default_factory=list)


@dataclass(frozen=True)
class FaqEntry:
    q: str
    a: str


@dataclass(frozen=True)
class FaqSection:
    type: str
    entries: list[FaqEntry] = field(default_factory=list)


@dataclass(frozen=True)
class GallerySection:
    type: str
    entries: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LyricsSection:
    type: str
    title: str
    lines: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LodgingEntry:
    name: str
    distance: str
    body: str
    rate: str
    special_rate: str | None = None
    savings: str | None = None
    href: str = "#"


@dataclass(frozen=True)
class LodgingSection:
    type: str
    title: str
    map_note: str
    entries: list[LodgingEntry] = field(default_factory=list)


@dataclass(frozen=True)
class Photos:
    slideshow: list[str]
    welcome_cover: str
    story_cover: str
    alt_cover: str


@dataclass(frozen=True)
class Page:
    slug: str
    title: str
    heading: str
    intro: str
    cover: str | None = None
    eyebrow: str | None = None
    sections: list[object] = field(default_factory=list)


@dataclass(frozen=True)
class WeddingSite:
    couple: str
    monogram: str
    greeting_tigrinya: str
    event_date_label: str
    event_location: str
    countdown_target_iso: str
    welcome_message: str
    rsvp_label: str
    accent_image: str
    nav: list[NavItem]
    photos: Photos
    pages: dict[str, Page]


SITE = WeddingSite(
    couple="Dn. Robel & Leah",
    monogram="R+L",
    greeting_tigrinya="ብሰላም ምጹ",
    event_date_label="Saturday, November 21, 2026",
    event_location="Colmar Manor, MD",
    countdown_target_iso="2026-11-21T00:00:00-05:00",
    welcome_message="We can’t wait to celebrate this sacred moment with you. Our union is more than a joining of lives...it is a reflection of love, faith, and divine timing. Surrounded by those we hold dear, we look forward to sharing a day filled with joy, gratitude, and spiritual connection. May this celebration be a reminder of the love that guides us all and the blessings that bring us together.",
    rsvp_label="Submit RSVP",
    accent_image="https://withjoy.com/assets/public/graphicAccents/accent_songket_gold_horizontal.png",
    nav=[
        NavItem("rsvp", "RSVP", "/rsvp"),
        NavItem("itinerary", "Itinerary", "/itinerary"),
        NavItem("travel", "Travel / Stay", "/travel"),
        NavItem("faq", "FAQ", "/faq"),
        NavItem("mezmur", "Mezmur", "/mezmur"),
        NavItem("moments", "Moments", "/moments"),
    ],
    photos=Photos(
        slideshow=[
            "/static/photos/couple-1.jpeg",
            "/static/photos/couple-2.jpeg",
            "/static/photos/couple-3.jpeg",
        ],
        welcome_cover="/static/photos/couple-1.jpeg",
        story_cover="/static/photos/couple-2.jpeg",
        alt_cover="/static/photos/couple-3.jpeg",
    ),
    pages={
        "welcome": Page(
            slug="welcome",
            title="Welcome",
            eyebrow="November 2026",
            heading="We’re honored to celebrate with you",
            intro="This space holds the key details for our wedding day: RSVP, travel and stay guidance, the full itinerary, frequently asked questions, mezmur lyrics, and shared moments.",
            sections=[
                CalloutSection(
                    type="callout",
                    title="Saturday, November 21, 2026",
                    body="Please use the tabs above to RSVP, plan your stay, review the itinerary, and keep up with updates as the celebration gets closer.",
                ),
                GridSection(
                    type="grid",
                    entries=[
                        GridEntry("Main Day", "Saturday, November 21"),
                        GridEntry("Ceremony", "Debre Selam MedhaneAlem Eritrean Orthodox Tewahdo Church"),
                        GridEntry("Reception", "Waterford Event Center"),
                    ],
                ),
            ],
        ),
        "rsvp": Page(
            slug="rsvp",
            title="RSVP",
            cover="welcome_cover",
            heading="RSVP",
            intro="Please fill out the form below so we can keep track of your response directly through the wedding site.",
            sections=[
                CalloutSection(
                    type="callout",
                    title="Respond Here",
                    body="Share your RSVP details below. Your response will be saved directly by the site so you do not need to leave this page.",
                )
            ],
        ),
        "itinerary": Page(
            slug="itinerary",
            title="Itinerary",
            cover="alt_cover",
            heading="Wedding Day Itinerary",
            intro="Saturday, November 21, 2026",
            sections=[
                EventSection(
                    type="events",
                    title="Saturday Celebration",
                    entries=[
                        EventEntry(
                            time="5:30 AM to 12:00 PM",
                            title="ቃል ኪዳን, ቅዳሴ / Wedding Ceremony, Liturgy",
                            location="Debre Selam MedhaneAlem Eritrean Orthodox Tewahdo Church, 4331 Bladensburg Rd, Colmar Manor, MD 20722, USA",
                            body="Please be at Debre Selam MedhaneAlem Eritrean Orthodox Tewahdo Church in Bladensburg, MD by 5:30 AM sharp!",
                        ),
                        EventEntry(
                            time="Dress Code",
                            title="ጻዕዳ ክዳን / White Clothes",
                            location="Ceremony",
                            body="Please wear white clothes for the liturgy and wedding ceremony.",
                        ),
                        EventEntry(
                            time="4:00 PM to 11:30 PM",
                            title="መርዓ ጽንብል / Wedding Reception",
                            location="Waterford Event Center, 6715 Commerce St, Springfield, VA 22150, USA",
                            body="Please be at the Waterford Event Center for the reception, which begins at 4 PM, and the bride and groom's entrance is at 5:30 PM.",
                        ),
                        EventEntry(
                            time="Dress Code",
                            title="ጻዕዳ ክዳን / White Clothes",
                            location="Reception",
                            body="Please wear white clothes for the wedding reception as well.",
                        ),
                    ],
                ),
                LinkSection(
                    type="links",
                    entries=[
                        LinkEntry("Church Location", "https://maps.google.com/?q=Debre+Selam+MedhaneAlem+Eritrean+Orthodox+Tewahdo+Church+4331+Bladensburg+Rd+Colmar+Manor+MD+20722", True),
                        LinkEntry("Reception Location", "https://maps.google.com/?q=Waterford+Event+Center+6715+Commerce+St+Springfield+VA+22150", True),
                        LinkEntry("Travel / Stay", "/travel"),
                    ],
                ),
            ],
        ),
        "travel": Page(
            slug="travel",
            title="Travel / Stay",
            cover="alt_cover",
            heading="Travel and Stay",
            intro="Travel planning notes, airport guidance, local transportation, and hotel ideas for the wedding weekend.",
            sections=[
                GridSection(
                    type="grid",
                    entries=[
                        GridEntry("Closest Airport", "Ronald Reagan Washington National Airport (DCA) is the most convenient airport for guests staying near the church or heading into D.C."),
                        GridEntry("Other Airport Options", "Baltimore/Washington International Thurgood Marshall Airport (BWI) and Washington Dulles International Airport (IAD) are both options if flights are better priced."),
                        GridEntry("Getting Around", "Uber and Lyft are the easiest options for most guests. Renting a car can help if you plan to stay farther out or move between Maryland and Virginia on the wedding day."),
                    ],
                ),
                LodgingSection(
                    type="lodging",
                    title="Hotel Ideas",
                    map_note="Choose a hotel near Colmar Manor for the ceremony or near Springfield for the reception if you want a shorter evening return.",
                    entries=[
                        LodgingEntry(
                            name="Wyndham Garden Washington DC Area",
                            distance="1.4 mi from the church",
                            body="A practical option for guests who want to stay close to the morning ceremony location in Colmar Manor.",
                            rate="$104",
                            special_rate="$100",
                        ),
                        LodgingEntry(
                            name="Holiday Inn Express Washington DC - BW Parkway by IHG",
                            distance="1.8 mi from the church",
                            body="Useful for guests who want a simple, familiar stay with breakfast included and convenient roadway access.",
                            rate="$121",
                        ),
                        LodgingEntry(
                            name="Hilton Springfield",
                            distance="16.8 mi from the church / near reception area",
                            body="A stronger fit if you prefer to stay closer to the reception venue in Springfield for the evening portion of the day.",
                            rate="$99",
                            special_rate="$95",
                        ),
                    ],
                ),
            ],
        ),
        "faq": Page(
            slug="faq",
            title="FAQ",
            cover="story_cover",
            heading="Frequently Asked Questions",
            intro="A few quick answers to common questions from guests.",
            sections=[
                FaqSection(
                    type="faq",
                    entries=[
                        FaqEntry("What’s the RSVP deadline?", "Please RSVP by September 30th to get an accurate headcount. :)"),
                        FaqEntry("Can I bring a friend?", "Due to the intimate nature of our venue and limited capacity, we’re only able to accommodate the guests formally listed on each invitation. We truly appreciate your understanding and look forward to celebrating together."),
                        FaqEntry("Are kids welcome?", "Yes!"),
                        FaqEntry("Where can I park?", "There are lots of free parking spaces."),
                        FaqEntry("Are the ceremony and reception spaces wheelchair accessible?", "Yes!"),
                        FaqEntry("What should I wear?", "Check our Schedule for dress code details."),
                        FaqEntry("What shoes should I wear (or avoid)?", "Check our Schedule for dress code details."),
                        FaqEntry("Who should I contact if I have questions?", "If you have any questions, please reach out to our wonderful wedding coordinator, Tsion...."),
                        FaqEntry("What will the weather be like?", "Welcome to the DMV, everyone visiting from out of town. The weather here can be unpredictable. Expect cool to mild weather, usually around 50 to 60 degrees, but it gets chilly at night. Please pack some warm layers for the evenings."),
                        FaqEntry("Is the wedding indoors or outdoors?", "Our wedding ceremony and reception will both be indoors."),
                        FaqEntry("Can we take photos with our phones and cameras during the wedding?", "Yes! We would love for you to take photos and share them. Please do not take photos during Liturgy."),
                    ],
                ),
            ],
        ),
        "mezmur": Page(
            slug="mezmur",
            title="Mezmur",
            cover="story_cover",
            heading="Mezmur",
            intro="Words for guests to read and sing along with during the celebration.",
            sections=[
                LyricsSection(
                    type="lyrics",
                    title="ዘምሩ ለአምላክነ",
                    lines=[
                        "ዘምሩ ለአምላክነ ዘምሩ /2/",
                        "ዘምሩ ለንጉሥነ ዘምሩ /2/ /2/",
                    ],
                )
            ],
        ),
        "moments": Page(
            slug="moments",
            title="Moments",
            cover="story_cover",
            heading="Moments",
            intro="A place to keep adding photos that capture the moments leading into and surrounding the wedding.",
            sections=[
                GallerySection(
                    type="gallery",
                    entries=[
                        "https://withjoy.com/media/ee0af8d08e6641499ba9405f52366110746d97d46863c126c/efdc1780-3f78-11f1-bd7b-071803ff6725-PIC05606.jpg?rendition=medium",
                        "https://withjoy.com/media/ee0af8d08e6641499ba9405f52366110746d97d46863c126c/aa7f19f0-3ec2-11f1-8716-2d8f095304d6-0.jpg?rendition=medium",
                        "https://withjoy.com/media/ee0af8d08e6641499ba9405f52366110746d97d46863c126c/a0dec730-3ec5-11f1-8e2d-eb3b96bde2d9-unnamed.jpg?rendition=medium",
                    ],
                )
            ],
        ),
    },
)


PAGE_ROUTES = {
    "welcome": "/",
    "rsvp": "/rsvp",
    "itinerary": "/itinerary",
    "travel": "/travel",
    "faq": "/faq",
    "mezmur": "/mezmur",
    "moments": "/moments",
}


def get_page(slug: str) -> Page:
    return SITE.pages[slug]
