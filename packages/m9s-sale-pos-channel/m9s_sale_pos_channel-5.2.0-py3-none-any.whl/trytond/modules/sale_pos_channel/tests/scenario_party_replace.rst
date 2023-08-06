======================
Party Replace Scenario
======================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard, Report
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Install sale_pos_channel::

    >>> config = activate_modules(['party', 'sale_pos_channel'])

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> cash = accounts['cash']
    >>> receivable = accounts['receivable']

Create tax::

    >>> tax = create_tax(Decimal('.10'))
    >>> tax.save()

Create parties::

    >>> Party = Model.get('party.party')
    >>> party = Party(name='Customer')
    >>> party.save()
    >>> party2 = Party(name='Customer')
    >>> party2.save()

Create category::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name='Category')
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.account_revenue = revenue
    >>> account_category.customer_taxes.append(tax)
    >>> account_category.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> Product = Model.get('product.product')
    >>> product = Product()
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.purchasable = True
    >>> template.salable = True
    >>> template.list_price = Decimal('10')
    >>> template.account_category = account_category
    >>> product, = template.products
    >>> product.cost_price = Decimal('5')
    >>> template.save()
    >>> product, = template.products

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create price list::

    >>> PriceList = Model.get('product.price_list')
    >>> price_list = PriceList()
    >>> price_list.name = 'Default price list'
    >>> price_list.save()

Create a POS channel::

    >>> Channel = Model.get('sale.channel')
    >>> Location = Model.get('stock.location')
    >>> warehouse, = Location.find([
    ...         ('code', '=', 'WH'),
    ...         ])
    >>> channel = Channel()
    >>> channel.name = 'Local channel'
    >>> channel.source = 'pos'
    >>> channel.pos_party = customer
    >>> channel.address = company.party.addresses[0]
    >>> channel.warehouse = warehouse
    >>> channel.shipment_method = 'order'
    >>> channel.invoice_method = 'order'
    >>> channel.payment_term = payment_term
    >>> channel.price_list = price_list
    >>> channel.save()

Create journals::

    >>> Sequence = Model.get('ir.sequence')
    >>> Journal = Model.get('account.journal')
    >>> StatementJournal = Model.get('account.statement.journal')
    >>> sequence = Sequence(name='Satement',
    ...     code='account.journal',
    ...     company=company,
    ... )
    >>> sequence.save()
    >>> account_journal = Journal(name='Statement',
    ...     type='statement',
    ...     sequence=sequence,
    ... )
    >>> account_journal.save()
    >>> statement_journal = StatementJournal(name='Default',
    ...     journal=account_journal,
    ...     account=cash,
    ...     validation='balance',
    ... )
    >>> statement_journal.save()

Create a device::

    >>> Device = Model.get('sale.device')
    >>> device = Device()
    >>> device.channel = channel
    >>> device.name = 'Default'
    >>> device.journals.append(statement_journal)
    >>> device.journal = statement_journal
    >>> device.save()

Reload the context::

    >>> User = Model.get('res.user')
    >>> Group = Model.get('res.group')
    >>> user, = User.find([('login', '=', 'admin')])
    >>> user.sale_device = device
    >>> user.current_channel = channel
    >>> user.save()
    >>> config._context = User.get_preferences(True, config.context)

Create an Inventory::

    >>> Location = Model.get('stock.location')
    >>> Inventory = Model.get('stock.inventory')
    >>> InventoryLine = Model.get('stock.inventory.line')
    >>> storage, = Location.find([
    ...         ('code', '=', 'STO'),
    ...         ])
    >>> inventory = Inventory()
    >>> inventory.location = storage
    >>> inventory.save()
    >>> inventory_line = InventoryLine(product=product, inventory=inventory)
    >>> inventory_line.quantity = 100.0
    >>> inventory_line.expected_quantity = 0.0
    >>> inventory.save()
    >>> inventory_line.save()
    >>> Inventory.confirm([inventory.id], config.context)
    >>> inventory.state == 'done'
    True

Create a POS sale::

    >>> Sale = Model.get('sale.sale')
    >>> SaleLine = Model.get('sale.line')
    >>> sale = Sale()
    >>> sale.channel == channel
    True
    >>> sale.party == customer
    True
    >>> sale.payment_term == payment_term
    True
    >>> sale.price_list == price_list
    True
    >>> sale.invoice_method == 'order'
    True
    >>> sale.shipment_method == 'order'
    True
    >>> sale.self_pick_up == True
    True
    >>> sale_line = sale.lines.new()
    >>> sale_line.product = product
    >>> sale_line.quantity = 2.0
    >>> sale.save()
    >>> sale_line, = sale.lines
    >>> sale_line.unit_price_w_tax
    Decimal('11.000000')
    >>> sale_line.amount_w_tax
    Decimal('22.00')
    >>> len(sale.shipments), len(sale.invoices), len(sale.payments)
    (0, 0, 0)

Try replace active party::

    >>> replace = Wizard('party.replace', models=[party])
    >>> replace.form.source = party
    >>> replace.form.destination = party2
    >>> replace.execute('replace')

Check fields have been replaced::

    >>> sale.reload()
    >>> sale.party == party2
    True
