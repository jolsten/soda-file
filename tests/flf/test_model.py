import pytest
from sodafile.flf import FLF, FLFReader

template1 = """
VOLUME      CLASSIFICATION=UNCLASSIFIED NUMBER=123456789 CREATION=020329        
            {volume_byte}                                                           
FILE        CLASSIFICATION=UNCLASSIFIED NUMBER=123456789 CREATION=020329        
            BLOCK=4096 RBPL=2 RBRP=3 {file_byte}                             
EVENT       VEHICLE=TSAT DATE=001210 SPUT=TSAT ORBIT=00000 TYPE=TSAT            
SIGNAL      DESIGNATOR=S000N FREQUENCY=1000.0 UPTIME=121800 DOWNTIME=122640     
INPUT       COLLECTOR=TEST ANALOG=NONE                                          
SELECTOR    NUMBER=1                                                            
PROCESSOR   NAME=SASI VERSION=1 TYPE=INTERNAL CHANNELS=128 NOMINAL=255          
            RATE=10.0                                                           
RECORD      RRLN=70 RRPL=6 AUXILIARY=TIM1,TIM2,TIM3,TIMP WORD=8 RDPL=0 RDRC=1   
            RDID=10 RDES=128 RDST=1 RDIN=1                                      
OUTPUT      TYPE=PCM                                                            
"""


@pytest.mark.parametrize(
    "volume, file, result",
    [
        ("MSBF", None, "MSBF"),
        (None, "MSBF", "MSBF"),
        ("LSBF", None, "LSBF"),
        (None, "LSBF", "LSBF"),
    ],
)
def test_flf_byteorder(volume, file, result):
    text = template1.format(
        volume_byte=f"BYTE={volume}" if volume else "",
        file_byte=f"BYTE={file}" if file else "",
    )
    print(text)
    reader = FLFReader.from_text(text)
    print(reader)
    # flf = FLF(**reader.to_dict())
    # assert flf.byte_order == result
