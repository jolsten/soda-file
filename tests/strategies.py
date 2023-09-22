from typing import List
from hypothesis import strategies as st, assume

SECTIONS = [
    "VOLUME",
    "FILE",
    "EVENT",
    "SIGNAL",
    "INPUT",
    "SELECTOR",
    "PROCESSOR",
    "RECORD",
    "OUTPUT",
]
INDENT_SIZE = max([len(sect) for sect in SECTIONS]) + 1


@st.composite
def section_names(draw, sections: List[str] = SECTIONS):
    return draw(st.sampled_from(sections))


@st.composite
def keys(draw, min_size: int = 3, max_size: int = 10):
    x = draw(
        st.text(
            alphabet=st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            min_size=min_size,
            max_size=max_size,
        )
    )
    return x.upper()


@st.composite
def values(draw, min_size: int = 1, max_size: int = 20):
    x = draw(
        st.text(
            alphabet=st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ_-,"),
            min_size=min_size,
            max_size=max_size,
        )
    )
    return x.upper()


@st.composite
def key_val_pairs(
    draw,
    min_key_size: int = 3,
    max_key_size: int = 10,
    min_val_size: int = 1,
    max_val_size: int = 20,
):
    key = draw(keys(min_size=min_key_size, max_size=max_key_size)).upper()
    val = draw(values(min_size=min_val_size, max_size=max_val_size)).upper()
    kvp = f"{key}={val}"
    return kvp


@st.composite
def key_val_dict(draw, min_size: int = 1, max_size: int = 10):
    return draw(st.dictionaries(keys(), values(), min_size=min_size, max_size=max_size))


@st.composite
def unwrapped_sections(draw, min_kvp: int = 1, max_kvp: int = 10):
    section = draw(section_names())
    kvpairs = draw(
        st.lists(
            key_val_pairs(),
            min_size=min_kvp,
            max_size=max_kvp,
            unique_by=lambda x: x.split("=", maxsplit=1)[0],
        )
    )
    joined = " ".join(kvpairs)
    unwrapped = f"{section: <{INDENT_SIZE}}{joined}"
    return unwrapped
