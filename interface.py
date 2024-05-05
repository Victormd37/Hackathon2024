from flet import *
#from talk import run_mike

def main(page: Page):

    ''' PÀGINA PRINCIPAL '''

    BLUE1 = '#003366'
    BLUE2 = '#0047AB'
    BLUE3 = '#001F3F'

    # Continguts de la main page 
    top_line = ResponsiveRow(
        controls = [
            Container(
                content=Text(value='Welcome to the SEIDOR\'s voice assistant', size=30, color='white', font_family='regular',weight='w700',text_align='center')  
            )
        ]
    )

    c_esp=Container(height=20)

    dialog = Container(
        width=500,
        height=400,
        padding=padding.only(
            top=20,right=10,
            left=10
        ),
        bgcolor='#09052A',
        border_radius=15,
        content=Column(
            scroll=True,
            controls=[
                Row(
                    alignment='start',
                    controls=[
                        Column(
                            controls=[
                                Text(value='User', size=15, color='white', font_family='regular',weight= 'bold',text_align='start'),
                                Container(
                                    height= 60,
                                    width= 275,
                                    bgcolor=BLUE2,
                                    padding=padding.only(
                                        left=5, top=5,
                                        bottom=5
                                    ),
                                    border_radius=10,
                                    content=ResponsiveRow(
                                        alignment='start',
                                        controls=[
                                            Text(value='I want 5 units of GLUCANTIME 5x5ml, and 3 units of SCALIBOR PEQ 48cm', size=15, color='white',font_family='regular',text_align='start')
                                        ]
                                    )
                                )
                            ]
                        )
                        
                    ]
                ),
                Container(height=5),
                Row(
                    alignment='end',
                    controls=[
                        Column(
                            controls=[
                                Text(value='Karina', size=15, color='white', font_family='regular',weight= 'bold',text_align='start'),
                                Container(
                                    height= 60,
                                    width= 275,
                                    bgcolor=BLUE2,
                                    padding=padding.only(
                                        left=5, top=5,
                                        bottom=5
                                    ),
                                    border_radius=10,
                                    content=ResponsiveRow(
                                        alignment='start',
                                        controls=[
                                            Text(value='OK! Check your list and tell me if you want to modify something', size=15, color='white', font_family='regular',text_align='start')
                                        ]
                                    )
                                ),
                                Container(
                                    height= 60,
                                    width= 275,
                                    bgcolor=BLUE2,
                                    padding=padding.only(
                                        left=5, top=5,
                                        bottom=5
                                    ),
                                    border_radius=10,
                                    content=ResponsiveRow(
                                        alignment='start',
                                        controls=[
                                            Text(value='You can either delete products or add new ones', size=15, color='white', font_family='regular',text_align='start')
                                        ]
                                    )
                                )
                            ]
                        )
                        
                    ]
                ),
                Container(height=5),
                Row(
                    alignment='start',
                    controls=[
                        Column(
                            controls=[
                                Text(value='User', size=15, color='white', font_family='regular',weight= 'bold',text_align='start'),
                                Container(
                                    height= 60,
                                    width= 275,
                                    bgcolor=BLUE2,
                                    padding=padding.only(
                                        left=5, top=5,
                                        bottom=5
                                    ),
                                    border_radius=10,
                                    content=ResponsiveRow(
                                        alignment='start',
                                        controls=[
                                            Text(value='I want to add 2 more units of SCALIBOR PEQ 48cm', size=15, color='white', font_family='regular',text_align='start')
                                        ]
                                    )
                                )
                            ]
                        )
                        
                    ]
                ),
                Container(height=5),
                Row(
                    alignment='end',
                    controls=[
                        Column(
                            controls=[
                                Text(value='Karina', size=15, color='white', font_family='regular',weight= 'bold',text_align='start'),
                                Container(
                                    height= 30,
                                    width= 275,
                                    bgcolor=BLUE2,
                                    padding=padding.only(
                                        left=5, top=5,
                                        bottom=5
                                    ),
                                    border_radius=10,
                                    content=ResponsiveRow(
                                        alignment='start',
                                        controls=[
                                            Text(value='List already modified!', size=15, color='white', font_family='regular',text_align='start')
                                        ]
                                    )
                                )
                            ]
                        )
                        
                    ]
                ),
                Container(height=10)
            ]     
        )
    )

    check_button = Row(
        alignment='center',
        controls=[
            Container(
                width = 200,
                height = 50,
                padding=padding.only(
                    top=10,right=10,
                    left=10,bottom=10
                ),
                bgcolor = '#12A995',
                border_radius=10,
                on_click=lambda _: page.go('/check_list'),
                content= ResponsiveRow(
                    alignment='center',
                    controls=[
                        Text(value='Check your list', size=20, color='white', font_family='regular',weight='bold',text_align='center')
                    ]
                )
            )
        ]
    )

    record_voice_button = Row(
        alignment='center',
        controls=[
            Container(
                width=100,
                height=100,
                border_radius=70,
                bgcolor='white',
                content=Icon(icons.MULTITRACK_AUDIO,color='#12A995',size=50),
            )
        ]
    ) 
    
    # Columna main 
    main_col = Column()
    main_col.controls.append(top_line)
    main_col.controls.append(c_esp)
    main_col.controls.append(dialog)
    main_col.controls.append(c_esp)
    main_col.controls.append(check_button)
    main_col.controls.append(c_esp)
    main_col.controls.append(record_voice_button)
    
    
    # Visualització de la main page
    main_page = Container( 
        width=400,
        height=850,
        padding=padding.only(
            top=50,right=25,
            left=25
        ),
        gradient=LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=[BLUE1,BLUE2,BLUE3]
        ),
        border_radius=15,
        content=main_col
    )

    
    ''' PÀGINA SECUNDÀRIA '''

    # Continguts de la segona pàgina
    top_second_line = Row(
        alignment='start',
        controls=[
            Container(
                on_click=lambda _: page.go('/'),
                content=Text(value='X', size=20, color='white', font_family='regular',weight='bold',text_align='center')
            )
        ]
    )

    second_line = Row(
        alignment='center',
        controls=[
            Text(value='LIST', size=30, color='white', font_family='regular',weight='w700',text_align='center')
        ]  
    )
    llista = Row(alignment='center',
                    controls=[
                        DataTable(column_spacing=30,data_row_max_height=30,data_row_min_height=15,heading_row_height=35,horizontal_lines=border.BorderSide(1,'white'),
                            columns=[
                                DataColumn(Text(value='PRODUCT',color= 'white',font_family='Arial',weight='w700')),
                                DataColumn(Text(value='QUANTITY',color='white',font_family='Arial',weight='w700'))
                            ],
                            rows=[
                                DataRow(
                                    cells=[
                                        DataCell(Text(value='GLUCANTIME 5x5ml',color= 'white',font_family='Regular')),
                                        DataCell(Text(value='5',color= 'white',font_family='Regular'))
                                    ]
                                ),
                                DataRow(
                                    cells=[
                                        DataCell(Text(value='SCALIBOR PEQ 48cm',color= 'white',font_family='Regular')),
                                        DataCell(Text(value='5',color= 'white',font_family='Regular'))
                                    ]
                                ),
                            ]
                        )
                    ]
                )
    
    line_secondary4 = Row(
        alignment='center',
        controls=[
            Text(value='PICKING STRATEGY', size=30, color='white', font_family='regular',weight='w700',text_align='center')
        ]  
    ) 

    last = Row(
        alignment='center',
        controls=[
            Container(
                width=300,
                height=300,
                border_radius=15,
                content= Image('C:/Users/rions/UPC/Hackathon/Alternativa/camino_optimo.gif',fit=ImageFit.COVER)
            )
           
        ]
    )
    
    # Columna de la segona pàgina
    secondary_col = Column()
    secondary_col.controls.append(top_second_line)
    secondary_col.controls.append(Container(height=50))
    secondary_col.controls.append(second_line)
    secondary_col.controls.append(Container(height=10))
    secondary_col.controls.append(llista)
    secondary_col.controls.append(Container(height=70))
    secondary_col.controls.append(line_secondary4)
    secondary_col.controls.append(Container(height=20))
    secondary_col.controls.append(last)


    # Visualització de la segona pàgina
    check_list = Container( 
        width=400,
        height=850,
        padding=padding.only(
            top=15,right=15,
            left=15
        ),
        gradient=LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=[BLUE1,BLUE2,BLUE3]
        ),
        border_radius=15,
        content=secondary_col
    )

    # Diccionari de pàgines
    pages = {
      '/':View(
                "/",
                [
                   main_page
                ],
            ),
      '/check_list': View(
                    "/check_list",
                    [
                        check_list
                    ],
                )
            
    }
    
    
    # Funció de navegació 
    def route_change(route):
        page.views.clear()
        page.views.append(pages[page.route])

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    app(target=main)