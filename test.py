# import streamlit_authenticator as stauth
import streamlit as st
import pandas as pd
import math
import os
st.set_page_config(layout="wide")

if "df" not in st.session_state:
  if os.path.exists("Rate.csv"):
      st.session_state["df"]=pd.read_csv("Rate.csv")
  else:
      st.session_state["df"]=pd.read_csv("rate_.csv")
      st.session_state["df"].to_csv("Rate.csv",index=False)
rate_df=st.session_state["df"]

@st.cache_data
def carrugation_price_Material(stock,w_s,l_s,laminate_sheet,Machine):
    if stock=="None":
        return 0
    elif stock=="L1":
        return int(w_s*l_s*laminate_sheet/2400*Machine["L1"].iloc[0])
    elif stock=="E Flute":
        return int(w_s*l_s*laminate_sheet/2400*Machine["E-flute"].iloc[0])
    elif stock=="B Flute":
        return int(w_s*l_s*laminate_sheet/2400*Machine["B-flute"].iloc[0])
    else:
        return 0
@st.cache_data
def EmbossBlock_price(Emboss,w_p,l_p,Machine):  
    if Emboss=="Yes":
        return int(w_p*l_p*Machine["Emboss"].iloc[0]/3)
    else:
        return 0
@st.cache_data
def DebossBlock_price(Deboss,w_p,l_p,Machine):
    if Deboss=="Yes":
        return int(w_p*l_p*Machine["Deboss"].iloc[0]/3)
    else:
        return 0
@st.cache_data
def foil_block_price(foiling,w_p,l_p,Machine):
    if foiling=="Yes":
        # print(w_p)
        return int(w_p*l_p*Machine["Foil_Price"].iloc[0]/3)
    else:
        return 0
@st.cache_data
def Die_making_price(machine):
    return machine["Die Making"].iloc[0]

@st.cache_data
def paper_material(w_s,l_s,gms,print_sheet,material,Machine,):
    if gms<=350 and material=="Bleach Card":
        return int(w_s*l_s*gms/15500*print_sheet/100*(Machine["SBS"].iloc[0]))
    elif gms>350 and material=="Bleach Card":
        return int(w_s*l_s*gms/15500*print_sheet/100*(Machine["SBSP"].iloc[0]))
    elif gms<=350 and material=="Bux Board":
        return int(w_s*l_s*gms/15500*print_sheet/100*(Machine["BB"].iloc[0]))
    elif gms>350 and material=="Bux Board":
        return int(w_s*l_s*gms/15500*print_sheet/100*(Machine["BBP"].iloc[0]))
    elif gms<=350 and material=="Kraft":
        return int(w_s*l_s*gms/15500*print_sheet/100*(Machine["Kraft"].iloc[0]))
    elif gms>350 and material=="Kraft":
        return int(w_s*l_s*gms/15500*print_sheet/100*(Machine["Kraft_P"].iloc[0]))
    elif gms<=350 and material=="Art Card":
        return int(w_s*l_s*gms/15500*print_sheet/100*(Machine["Art Card"].iloc[0]))
    elif gms>350 and material=="Art Card":
        return int(w_s*l_s*gms/15500*print_sheet/100*(Machine["Art Card_P"].iloc[0]))
    else:
        return 0

@st.cache_data
def CTP_Plates_price(Machine,process_color,pantone_color,matallic_color):
    try:
        # print(process_color,pantone_color,matallic_color)
        return Machine["Price/kg"].iloc[0]*(process_color+pantone_color+matallic_color)
    except Exception as e:
        # print(e)
        return 0

@st.cache_data
def corgation_price(w_s,l_s,pasting,Lamination_sheet,Machine):
    try:
        if pasting=="Single Side":
            return int(w_s*l_s*Machine["carugation_pasting_rate"].iloc[0]*Lamination_sheet/2400)
        elif pasting=="Double Side":
            return int(2*w_s*l_s*Machine["carugation_pasting_rate"].iloc[0]*Lamination_sheet/2400)
    except Exception as e:
        return 0
@st.cache_data
def embosing_price(w_p,l_p,Emboss,Machine,print_sheet):
    try:
        if Emboss=="Yes":
        # as printing rate is per 1170 and below list show us that if printing rate is 1400 and we have sheets 3350 it is below 4387 so we multply its index+1 to rate
            sheet_list =[1170, 2310, 3300, 4387, 5360, 6405, 7500, 8500, 9532, 10529, 11500, 12500, 13553, 14595, 15742, 16680, 17723, 18765, 19808, 20850, 21893, 22935, 23978, 25020, 26167, 27105, 28252, 29294, 30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719]
            for i in sheet_list:
                if print_sheet<=i:
                    factor=sheet_list.index(i)+1
                    break
            return Machine["Embos"].iloc[0]*factor
    except:
        return 0
@st.cache_data
def debosing_price(w_p,l_p,Debosing,Machine,print_sheet):
    try:
        if Debosing=="Yes":
        # as printing rate is per 1170 and below list show us that if printing rate is 1400 and we have sheets 3350 it is below 4387 so we multply its index+1 to rate
            sheet_list =[1170, 2310, 3300, 4387, 5360, 6405, 7500, 8500, 9532, 10529, 11500, 12500, 13553, 14595, 15742, 16680, 17723, 18765, 19808, 20850, 21893, 22935, 23978, 25020, 26167, 27105, 28252, 29294, 30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719]
            for i in sheet_list:
                if print_sheet<=i:
                    factor=sheet_list.index(i)+1
                    break
            return Machine["Debos"].iloc[0]*factor
    except:
        return 0
@st.cache_data
def foil_price(w_p,l_p,Foil,laminate_sheet,Machine):
    if Foil=="Yes":
        return int(w_p*l_p*laminate_sheet*Machine["Foil_Price"].iloc[0])
    else:
        return 0
    
def UV_price(w_s,l_s,UV,printable_quantity,Machine):
    try:
        if UV=="Yes":
            return int(w_s*l_s*printable_quantity*Machine["UV_price"].iloc[0])
        else:
            return 0
    except:
        return 0
@st.cache_data   
def Pasting_Calculator(Machine,Req_Q):
    try:
        thresholds = [
            1050, 2100, 3150, 4200, 5250, 6300, 7350, 8400, 9450, 10500,
            11500, 12500, 13500, 14500, 15500, 16500, 17500, 18500, 19600,
            20700, 21700, 22700, 23978, 25020, 26167, 27105, 28252, 29294,
            30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719
        ]
        for i, threshold in enumerate(thresholds, start=1):
            if Req_Q <= threshold:
                factor=i
                break
        return Machine["Pasting"].iloc[0]*i
    except:
        return 0
@st.cache_data
def Die_cut_price(Machine):
    try:
        # as printing rate is per 1170 and below list show us that if printing rate is 1400 and we have sheets 3350 it is below 4387 so we multply its index+1 to rate
        sheet_list =[1170, 2310, 3300, 4387, 5360, 6405, 7500, 8500, 9532, 10529, 11500, 12500, 13553, 14595, 15742, 16680, 17723, 18765, 19808, 20850, 21893, 22935, 23978, 25020, 26167, 27105, 28252, 29294, 30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719]
        for i in sheet_list:
            if print_sheet<=i:
                factor=sheet_list.index(i)+1
                break
        return Machine["Die Cut"].iloc[0]*factor
    except:
        return 0
@st.cache_data
def Lamination_sheets_calculator(sheet):
    try:
        if sheet <= 100:
            return math.ceil(sheet * 0.5 + sheet)
        elif sheet <= 200:
            return math.ceil(sheet * 0.5 + sheet)
        elif sheet <= 300:
            return math.ceil(sheet * 0.4 + sheet)
        elif sheet <= 400:
            return math.ceil(sheet * 0.2 + sheet)
        elif sheet <= 500:
            return math.ceil(sheet * 0.2 + sheet)
        elif sheet <= 600:
            return math.ceil(sheet * 0.18 + sheet)
        elif sheet >= 650 and sheet <= 1000:
            return math.ceil(sheet * 0.15 + sheet)
        elif sheet >= 1000 and sheet <= 1500:
            return math.ceil(sheet * 0.1 + sheet)
        elif sheet >= 1500 and sheet <= 2000:
            return math.ceil(sheet * 0.12 + sheet)
        elif sheet >= 2000 and sheet <= 3000:
            return math.ceil(sheet * 0.08 + sheet)
        elif sheet >= 3000 and sheet <= 4000:
            return math.ceil(sheet * 0.04 + sheet)
        elif sheet >= 4000 and sheet <= 7000:
            return math.ceil(sheet * 0.04 + sheet)
        elif sheet > 7000:
            return math.ceil(sheet * 0.025 + sheet)
        else:
            return sheet
    except:
        return 0
@st.cache_data
def Print_Sheet_calculator(sheet):
    try:
        if sheet <= 100:
            return math.ceil(sheet * 1.5 + sheet)
        elif sheet <= 200:
            return math.ceil(sheet * 1.0 + sheet)
        elif sheet <= 300:
            return math.ceil(sheet * 0.65 + sheet)
        elif sheet <= 400:
            return math.ceil(sheet * 0.45 + sheet)
        elif sheet <= 500:
            return math.ceil(sheet * 0.35 + sheet)
        elif sheet <= 600:
            return math.ceil(sheet * 0.3 + sheet)
        elif sheet >= 700 and sheet <= 1000:
            return math.ceil(sheet * 0.17 + sheet)
        elif sheet >= 1000 and sheet <= 1500:
            return math.ceil(sheet * 0.15 + sheet)
        elif sheet >= 1500 and sheet <= 2000:
            return math.ceil(sheet * 0.15 + sheet)
        elif sheet >= 2000 and sheet <= 3000:
            return math.ceil(sheet * 0.1 + sheet)
        elif sheet >= 3000 and sheet <= 4000:
            return math.ceil(sheet * 0.08 + sheet)
        elif sheet >= 4000 and sheet <= 5000:
            return math.ceil(sheet * 0.07 + sheet)
        elif sheet <= 6000:
            return math.ceil(sheet * 0.05 + sheet)
        elif sheet <= 7000:
            return math.ceil(sheet * 0.05 + sheet)
        elif sheet <= 8000:
            return math.ceil(sheet * 0.05 + sheet)
        elif sheet <= 9000:
            return math.ceil(sheet * 0.045 + sheet)
        elif sheet <= 10000:
            return math.ceil(sheet * 0.0475 + sheet)
        elif sheet > 10000:
            return math.ceil(sheet * 0.0425 + sheet)
    except:
        return 0

@st.cache_data
def find_machine_size(w, l,rate_df):
    
    if (w <= 12.5 and l <= 18) or (l <= 12.5 and w <= 18):
        machine = rate_df[rate_df.Machine_size == "12x17"]
        # print("12x17")
    elif (w <= 25 and l <= 18) or (l <= 25 and w <= 18):
        machine = rate_df[rate_df.Machine_size == "23x17"]
        # print("23x17")
    elif (w <= 25 and l <= 36) or (l <= 25 and w <= 36):
        machine = rate_df[rate_df.Machine_size == "25x36"]
        # print("25x36")
    elif (w <= 28 and l <= 40) or (l <= 28 and w <= 40):
        machine = rate_df[rate_df.Machine_size == "28x40"]
        # print("28x40")
    elif (w <= 35 and l <= 45) or (l <= 35 and w <= 45):
        machine = rate_df[rate_df.Machine_size == "35x45"]
        # print("35x45")
    elif (w <= 40 and l <= 60) or (l <= 40 and w <= 60):
        machine = rate_df[rate_df.Machine_size == "40x56"]
        # print("40x56")
    else:
        # print("No matching machine size found.")
        machine = None
    return machine
    # st.dataframe(machine, hide_index=True)
@st.cache_data
def Printing_Calculator(Machine,cmyk,pms,met,print_sheet):
    try:
        # as printing rate is per 1170 and below list show us that if printing rate is 1400 and we have sheets 3350 it is below 4387 so we multply its index+1 to rate
        sheet_list =[1170, 2310, 3300, 4387, 5360, 6405, 7500, 8500, 9532, 10529, 11500, 12500, 13553, 14595, 15742, 16680, 17723, 18765, 19808, 20850, 21893, 22935, 23978, 25020, 26167, 27105, 28252, 29294, 30233, 31275, 32318, 33360, 34403, 35485, 36488, 37634, 38677, 39719]
        for i in sheet_list:
            if print_sheet<=i:
                factor=sheet_list.index(i)+1
                break
            # CMYK=Machine["CMYK"].iloc[0, 0]
        return Machine["CMYK"].iloc[0]*cmyk*factor,Machine["PMS"].iloc[0]*pms*factor,Machine["Met"].iloc[0]*met*factor
    except:
        return 0,0,0
@st.cache_data
def Lamination_price_calculator(w_p,l_p,Sheet_printable,inside_rate,outside_rate,rate_df):
    # Outside_rate=Inside_rate=0
    try:
        # print(rate_df[outside_rate][0])
        Outside_rate=rate_df[outside_rate][0]
    except:
        Outside_rate=0
    try:
        Inside_rate=rate_df[inside_rate][0]
    except:
        # print(inside_rate)
        Inside_rate=0
    # if Inside_rate!="None":
        # Inside_rate=rate_df[inside_rate][0]
    
    outside_lamination= int((w_p*l_p/144)*Outside_rate*Sheet_printable)
    inside_lamination= int((w_p*l_p/144)*Inside_rate*Sheet_printable)
    return outside_lamination,inside_lamination

@st.cache_data
def load_data(file,sheet_name):
    # Load your data into a DataFrame (replace 'your_data.csv' with your actual data source)
    data = pd.read_excel(file,sheet_name=sheet_name)
    data.fillna(0,inplace=True)
    return data
# rate_df=load_data("rate_database.xlsx",sheet_name="Sheet1")
material_df=load_data("rate_database.xlsx",sheet_name="Sheet2")
lab_df=load_data("rate_database.xlsx",sheet_name="Sheet3")
# custom_css = f"""
#     <style>
#         .css-6qob1r.e1akgbir3 {{
#             color: firebrick;
#             background-color: black;
#         }}
#         .css-1629p8f.eqr7zpz1 >h2{{
#             color: firebrick;
#         }}
#     </style>
# """


# Apply custom CSS to change sidebar width
# st.markdown(custom_css, unsafe_allow_html=True)
# custom_css = f"""
#     <style>
#         h2 {{
#             color: firebrick;
#         }}
#     </style>
# """

# # Apply custom CSS to change header color
# st.markdown(custom_css, unsafe_allow_html=True)


######## Client Data ###########
form=st.sidebar.form("Calculate Material and Labour")

# Input fields
form.header("Packaging Estimation Sheet")
form.header("Client Bio")
col1,col2=form.columns(2)
client_name=col1._text_input("Client Name")
CSR=col2._text_input("CSR Name")
col1,col2=form.columns(2)
client_email=col1._text_input("Client Email")
Phone=col2._text_input("Phone Number")


########### Sheet Data (Size) #############



form.header("Sheet Size")
col1, col2 = form.columns(2)
W_S=col1.number_input("W_Sheet", min_value=0.0)

# st.write(W_S)

L_S=col2.number_input("L_Sheet", min_value=0.0)
# st.sidebar.header("Material")
col1, col2 = form.columns(2)
Material = col1.selectbox(
    "Material",
    ["Bleach Card","Bux Board", "Art Card", "Kraft",]
)
gsm = col2.number_input("GSM", min_value=0,value=300)
col1, col2 = form.columns(2)
up = col1.number_input("Box Uping", min_value=1)
Req_Q = col2.number_input("Required Quantity", min_value=0)


agree = form.checkbox('Print Size Same as Sheet Size')

form.header("Print Size")
col1, col2 = form.columns(2)
W_P=col1.number_input("W_Print", min_value=0.0)
L_P=col2.number_input("L_Print", min_value=0.0)
# st.sidebar.header("Material")

# Material_p = col1.selectbox(
#     "Material_Printing",
#     ["Bux Board", "Bleach Card", "Art Card", "Kraf",]
# )
# gsm_p = col2.number_input("GSM_Print", min_value=0)
# up_p = col1.number_input("Box Uping_Print", min_value=0)
# Req_Q_p= col2.number_input("Required Quantity_P", min_value=0)

form.header("Corrugation")
col1, col2 = form.columns(2)
stock = col1.selectbox(
    "Corrugation Material",
    ["None","L1", "E Flute", "B Flute"]
)

pasting = col2.selectbox(
    "Corrugation Pasting",
    ["None","Single Side", "Double Side",]
)

form.header("Printing Colors")
col1, col2, col3 = form.columns(3)
process_color = col1.selectbox(
    "Process Color",
    [0,1,2,3,4,5,6,7,8,]
)
pantone_color=col2.number_input("Pantone Color", min_value=0)
matallic_color=col3.number_input("Matallic Color", min_value=0)


form.header("Add-Ons")
col1, col2, col3,col4 = form.columns(4)
Foil = col1.selectbox(
    "Foiling",
    ["No","Yes",],
     index=0
)
Deboss = col2.selectbox(
    "Deboss",
     ["No","Yes",],
     index=0
)
Emboss = col3.selectbox(
    "Emboss",
     ["No","Yes",],
     index=0
)
UV = col4.selectbox(
    "UV",
     ["No","Yes",],
     index=0
)

window_die_cut=form.selectbox(
    "Window Diecut",
     ["None","With PVC","Without PVC",])
############ Lamination ##########
form.header("Lamination")
col1,col2=form.columns(2)
inside=col1.selectbox(
    "Inside Lamination",
     ["None","Matte","Gloss","Soft Touch","Varnish",])
outside=col2.selectbox(
    "Outside Lamination",
     ["None","Matte","Gloss","Soft Touch","Varnish",])

############ Additional Expense ##########

form.header("Additional Expense")
col1, col2 = form.columns(2)
Mics = col1.number_input("Micsellneus", min_value=0)
Profit_margin = col2.number_input("Profit Margin", min_value=0)


submitted = form.form_submit_button("Submit")

##################### Calculator ################################
if submitted:
    if agree:
        W_P=W_S
        L_P=L_S
    else:
        pass



    ### disply Machine size
    machine_rate=find_machine_size(W_S,L_S,rate_df)
    # st.dataframe(machine_rate,hide_index=True)
    Sheets=Req_Q/up
    print_sheet=Print_Sheet_calculator(Sheets)
    st.write(f'print_sheet: {print_sheet}')
    laminate_sheet=Lamination_sheets_calculator(Sheets)
    st.write(f'laminate_sheet: {laminate_sheet}')
    process_color_rate,pantone_color_rate,matallic_color_rate=Printing_Calculator(machine_rate,process_color,pantone_color,matallic_color,print_sheet)
    # st.write("Printing Rate")
    # st.write(process_color_rate,pantone_color_rate,matallic_color_rate)
    # st.write("Lamination Rate")
    lamination_price=Lamination_price_calculator(W_P,L_P,laminate_sheet,inside,outside,rate_df)
    # st.write(lamination_price)

    # st.write("Die Cut")
    die_cut_price=Die_cut_price(machine_rate)
    # st.write(die_cut_price)

    # st.write("Pasting")
    pasting_material=Pasting_Calculator(machine_rate,Req_Q)
    # st.write(pasting_material)
    # st.write("UV")
    UV_coating=UV_price(W_S,L_S,UV,print_sheet,machine_rate)
    # st.write(UV_coating)

    # st.write("Foil")
    foiling=foil_price(W_P,L_P,Foil,laminate_sheet,machine_rate)
    # st.write(foiling)
    # st.write("Debosing")
    Debosing=debosing_price(W_P,L_P,Deboss,machine_rate,print_sheet)
    # st.write(Debosing)
    # st.write("Embosing")
    Embosing=embosing_price(W_P,L_P,Emboss,machine_rate,print_sheet)
    # st.write(Embosing)

    # st.write("Carrugation")
    carrug_lab=corgation_price(W_S,L_S,pasting,laminate_sheet,machine_rate)
    # st.write(carrug_lab)
    lab_df.set_index('index',inplace=True)
    lab_df.loc["Printing"]=(process_color_rate,pantone_color_rate,matallic_color_rate,process_color_rate+pantone_color_rate+matallic_color_rate)
    lab_df.loc["Lam"]=(lamination_price[0],lamination_price[1],0,lamination_price[0]+lamination_price[1])
    lab_df.loc["Die cut"]=(die_cut_price,0,0,die_cut_price)
    lab_df.loc["Pasting"]=(pasting_material,0,0,pasting_material)
    lab_df.loc["Uv Coating"]=(UV_coating,0,0,UV_coating)
    lab_df.loc["Foiling"]=(foiling,0,0,foiling)
    lab_df.loc["Debossing"]=(Debosing,0,0,Debosing)
    lab_df.loc["Embossing"]=(Embosing,0,0,Embosing)
    lab_df.loc["Carrug Lab"]=(carrug_lab,0,0,carrug_lab)
    lab_df.loc["Lab Total"]=(0,0,0,lab_df.iloc[:-1,3].sum())

    lab_df.reset_index(inplace=True)
    # corgation_price(10,12.5,"Double Side",3467)

    ##################################
    ############ Material Calculation #############
    material_df.set_index('index',inplace=True)
    ctp=CTP_Plates_price(machine_rate,process_color,pantone_color,matallic_color)
    material_df.loc["CTP Plates"]=(0,0,0,ctp)
    paper_price=paper_material(W_S,L_S,gsm,print_sheet,Material,machine_rate)
    material_df.loc["Paper"]=(0,paper_price,0,paper_price)
    die_making_price=Die_making_price(machine_rate)
    material_df.loc["Die Making"]=(0,0,0,die_making_price)
    foil_block=foil_block_price(Foil,W_P,L_P,machine_rate)
    material_df.loc["Foil Block"]=(0,0,0,foil_block)
    deboss_price_Material=DebossBlock_price(Deboss,W_P,L_P,machine_rate)
    material_df.loc["DebossBlock"]=(0,0,0,deboss_price_Material)
    emboss_price_Material=EmbossBlock_price(Emboss,W_P,L_P,machine_rate)
    material_df.loc["EmbossBlock"]=(0,0,0,emboss_price_Material)
    Carrugation_price_Material=carrugation_price_Material(stock,W_S,L_S,laminate_sheet,machine_rate) ### Editing
    material_df.loc["Carrugation"]=(0,0,0,Carrugation_price_Material)
    material_df.loc["Material"]=(0,0,0,material_df.iloc[:-1,3].sum())

    material_df.reset_index(inplace=True)





###############################################
col1, col2, col3 = st.columns(3)
total=material_df.iloc[:-1,4].sum()+lab_df.iloc[:-1,4].sum()+Mics
Profit_margin=1+Profit_margin/100
total=total*Profit_margin
col1.metric("Total Amount", total, "Misc Profit Marig")
# col2.metric("Wind", "9 mph", "-8%")
if Req_Q==0:
    cost_per_piece=0
else:
    cost_per_piece=total/Req_Q
col3.metric("Cost Per Piece", cost_per_piece, "")

col1, col2, col3 = st.columns(3)
col1.metric("Material Cost", material_df.iloc[:-1,4].sum(), "")
col2.metric("Labour Cost", lab_df.iloc[:-1,4].sum(), "")
col3.metric("Mics", Mics, "")



col1,col2=st.columns(2)
n_rows=13
height = int(35.2*(n_rows+1))
col1.header("Material Cost")
col1.dataframe(material_df, width=700, height=410,hide_index=True)
col2.header("Labour Cost")
col2.dataframe(lab_df, width=700, height=height,hide_index=True)
# st.cache_data.clear()