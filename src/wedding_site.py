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
class Photos:
    trio: list[str]
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
    accent_image: str
    nav: list[NavItem]
    photos: Photos
    pages: dict[str, Page]


SITE = WeddingSite(
    couple="Robel & Leah",
    accent_image="https://withjoy.com/assets/public/graphicAccents/accent_songket_gold_horizontal.png",
    nav=[
        NavItem("welcome", "Welcome", "/"),
        NavItem("story", "Our Story", "/story"),
        NavItem("rsvp", "RSVP", "/rsvp"),
        NavItem("schedule", "Schedule", "/schedule"),
        NavItem("accommodations", "Where to Stay", "/accommodations"),
        NavItem("travel", "Travel", "/travel"),
        NavItem("faq", "Q&A", "/faq"),
        NavItem("moments", "Moments", "/moments"),
    ],
    photos=Photos(
        trio=[
            "https://withjoy.com/media/a8f33250-e301-5124-a382-e71c5db6312b/b8c535c0-3eb9-11f1-8259-3b566fd334f0-PIC05821.jpg?rendition=small",
            "https://withjoy.com/media/a8f33250-e301-5124-a382-e71c5db6312b/fbb62220-3ebb-11f1-8259-3b566fd334f0-PIC05841.jpg?rendition=small",
            "https://withjoy.com/media/a8f33250-e301-5124-a382-e71c5db6312b/b8c55cd0-3eb9-11f1-8259-3b566fd334f0-PIC05806.jpg?rendition=small",
        ],
        welcome_cover="https://withjoy.com/media/ee0af8d08e6641499ba9405f52366110746d97d46863c126c/efdc1780-3f78-11f1-bd7b-071803ff6725-PIC05606.jpg?rendition=medium",
        story_cover="https://withjoy.com/media/ee0af8d08e6641499ba9405f52366110746d97d46863c126c/aa7f19f0-3ec2-11f1-8716-2d8f095304d6-0.jpg?rendition=medium",
        alt_cover="https://withjoy.com/media/ee0af8d08e6641499ba9405f52366110746d97d46863c126c/a0dec730-3ec5-11f1-8e2d-eb3b96bde2d9-unnamed.jpg?rendition=medium",
    ),
    pages={
        "welcome": Page(
            slug="welcome",
            title="Welcome",
            eyebrow="July 2026",
            heading="Welcome to our wedding website",
            intro="We’re so happy you’re here. This site has the details you’ll need for the weekend, from travel and accommodations to the celebration schedule and RSVP information.",
            sections=[
                CalloutSection(
                    type="callout",
                    title="Join us in celebrating",
                    body="We created this space so friends and family can stay close to the details as the day approaches. Explore each page for plans, logistics, and photo moments from our story so far.",
                ),
                GridSection(
                    type="grid",
                    entries=[
                        GridEntry("Explore", "Our Story"),
                        GridEntry("Respond", "RSVP"),
                        GridEntry("Plan Ahead", "Travel + Stay"),
                    ],
                ),
            ],
        ),
        "story": Page(
            slug="story",
            title="Our Story",
            cover="story_cover",
            heading="Our Story",
            intro="A few favorite moments from our journey together.",
            sections=[
                TimelineSection(
                    type="timeline",
                    entries=[
                        TimelineEntry("The Beginning", "What started as an easy conversation turned into the kind of connection that kept unfolding naturally."),
                        TimelineEntry("Growing Together", "Through every season, we kept finding more reasons to choose each other with steadiness, joy, and faith."),
                        TimelineEntry("The Yes", "The next chapter became clear: gather the people we love and celebrate the life we’re building together."),
                    ],
                )
            ],
        ),
        "rsvp": Page(
            slug="rsvp",
            title="RSVP",
            cover="welcome_cover",
            heading="RSVP",
            intro="Please let us know if you’ll be joining us. We’re grateful for every effort made to celebrate with us.",
            sections=[
                CalloutSection(
                    type="callout",
                    title="Reply soon",
                    body="Use this page as the RSVP destination in the local version of the site. If you want, this can be wired to a real form or spreadsheet next.",
                )
            ],
        ),
        "schedule": Page(
            slug="schedule",
            title="Schedule",
            cover="alt_cover",
            heading="Schedule",
            intro="A simple outline for the wedding weekend.",
            sections=[
                TimelineSection(
                    type="timeline",
                    entries=[
                        TimelineEntry("Welcome Gathering", "An informal evening to greet friends and family arriving from near and far."),
                        TimelineEntry("Ceremony", "A joyful ceremony surrounded by the people who have shaped our lives."),
                        TimelineEntry("Reception", "Dinner, music, dancing, and time together to celebrate late into the evening."),
                    ],
                )
            ],
        ),
        "accommodations": Page(
            slug="accommodations",
            title="Where to Stay",
            cover="welcome_cover",
            heading="Where to Stay",
            intro="This page is designed for hotel and lodging details, including room blocks and booking guidance.",
            sections=[
                CalloutSection(
                    type="callout",
                    title="Hotel details",
                    body="Add the preferred hotel, room block code, neighborhood guidance, and parking notes here if you want the page filled with exact logistics next.",
                )
            ],
        ),
        "travel": Page(
            slug="travel",
            title="Travel",
            cover="alt_cover",
            heading="Travel",
            intro="Key planning details for getting in and around during the celebration weekend.",
            sections=[
                GridSection(
                    type="grid",
                    entries=[
                        GridEntry("Airport", "Nearest arrival option"),
                        GridEntry("Transit", "Rideshare, rental, or shuttle"),
                        GridEntry("Arrival", "Plan extra time for weekend traffic"),
                    ],
                )
            ],
        ),
        "faq": Page(
            slug="faq",
            title="Q&A",
            cover="story_cover",
            heading="Q&A",
            intro="Helpful details guests usually ask about before the wedding.",
            sections=[
                FaqSection(
                    type="faq",
                    entries=[
                        FaqEntry("What should I wear?", "Cocktail or formal attire works well unless a more specific dress code is added."),
                        FaqEntry("Can I bring a guest?", "Please follow the names included on your invitation and RSVP."),
                        FaqEntry("Will there be parking?", "Parking and arrival guidance can be added here once venue logistics are finalized."),
                    ],
                )
            ],
        ),
        "moments": Page(
            slug="moments",
            title="Moments",
            cover="story_cover",
            heading="Moments",
            intro="A photo-led page for favorite memories and future guest uploads.",
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
    "story": "/story",
    "rsvp": "/rsvp",
    "schedule": "/schedule",
    "accommodations": "/accommodations",
    "travel": "/travel",
    "faq": "/faq",
    "moments": "/moments",
}


def get_page(slug: str) -> Page:
    return SITE.pages[slug]
